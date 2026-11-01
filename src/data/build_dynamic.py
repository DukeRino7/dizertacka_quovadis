"""Normalizovaná cache Speakeasy reportov (deterministická, nič sa neučí) -> processed/dynamic/cache/.

Jedna vzorka (SHA-256) = jeden riadok so všetkými vstupnými bodmi a vláknami v poradí reportu.
Poradie riadkov v každej časti = poradie v processed/index/samples.parquet (rovnaké ako pri statických dátach).

Spustenie (po stiahnutí celého datasetu a po audite):
    .venv\\Scripts\\python.exe -m src.data.build_dynamic
Vývojová kontrola na časti dát:
    .venv\\Scripts\\python.exe -m src.data.build_dynamic --splits test --out <priečinok> --allow-missing --limit 500

Súbory pre každú časť <split> ∈ {train, validation, test}:
    <split>.parquet       sha256, family, label, status, súhrnné počty, ep_types, ep_lengths, ep_errors,
                          api_seq (postupnosť názvov API, celá vzorka), events (udalosti)
    <split>_args.parquet  sha256, api_args (argumenty každého volania spojené znakom '|' a orezané) – voliteľné
"""
import argparse
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from src.common.config import load_config
from src.common.paths import INDEX_DIR, PROCESSED_DIR, SPEAKEASY_DIR, rel
from src.common.provenance import describe_files, environment, git_info, now_iso, sha256_file, write_json
from .speakeasy_source import find_reports, parse_report, summarize

SPLIT_ORDER = ["train", "validation", "test"]
CHUNK = 4000


def _work(item, lowercase: bool, max_arg_chars: int, keep_args: bool):
    path, sha = item
    r = parse_report(SPEAKEASY_DIR / path, sha)
    row = summarize(r)
    norm = (lambda s: s.lower()) if lowercase else (lambda s: s)
    row.update({
        "ep_types": [ep.ep_type for ep in r.entry_points],
        "ep_lengths": [len(ep.api_names) for ep in r.entry_points],
        "ep_errors": [ep.error_type or "" for ep in r.entry_points],
        "api_seq": [norm(n) for ep in r.entry_points for n in ep.api_names],
        "events": [e for ep in r.entry_points for e in ep.events],
    })
    args = None
    if keep_args:
        args = ["|".join(a)[:max_arg_chars] for ep in r.entry_points for a in ep.api_args]
    return row, args


def build_split(part: pd.DataFrame, out: Path, split: str, ccfg: dict) -> dict:
    work = partial(_work, lowercase=ccfg["lowercase_api"], max_arg_chars=ccfg["max_arg_chars"], keep_args=ccfg["keep_args"])
    writer = args_writer = None
    n, status = 0, {}
    with ProcessPoolExecutor(max_workers=ccfg["workers"]) as ex:
        for start in range(0, len(part), CHUNK):
            chunk = part.iloc[start:start + CHUNK]
            res = list(ex.map(work, zip(chunk["path"], chunk["sha256"]), chunksize=32))
            rows = pd.DataFrame([r for r, _ in res])
            rows.insert(1, "family", chunk["family"].to_numpy())
            rows.insert(2, "label", chunk["label"].to_numpy())
            assert (rows["sha256"].to_numpy() == chunk["sha256"].to_numpy()).all()
            table = pa.Table.from_pandas(rows, preserve_index=False)
            writer = writer or pq.ParquetWriter(out / f"{split}.parquet", table.schema, compression="zstd")
            writer.write_table(table)
            if ccfg["keep_args"]:
                at = pa.table({"sha256": rows["sha256"], "api_args": [a for _, a in res]})
                args_writer = args_writer or pq.ParquetWriter(out / f"{split}_args.parquet", at.schema, compression="zstd")
                args_writer.write_table(at)
            for s, c in rows["status"].value_counts().items():
                status[s] = status.get(s, 0) + int(c)
            n += len(rows)
            print(f"  {split}: {n}/{len(part)}", flush=True)
    writer.close()
    if args_writer:
        args_writer.close()
    return {"rows": n, "status": status}


def main(splits, out: Path, allow_missing: bool, limit: int | None, cfg_path: str):
    t0 = time.perf_counter()
    ccfg = load_config(cfg_path)["cache"]
    out.mkdir(parents=True, exist_ok=True)
    index = pd.read_parquet(INDEX_DIR / "samples.parquet")
    disk = find_reports()[["sha256", "original_split", "path"]]
    m = index.merge(disk, on=["sha256", "original_split"], how="left")
    missing = m["path"].isna()
    if missing.any() and not allow_missing:
        raise SystemExit(f"{int(missing.sum())} vzoriek indexu nemá report – dokončiť sťahovanie (alebo --allow-missing pri vývoji).")
    info = {}
    for split in splits:
        part = m[(m["split"] == split) & ~missing].reset_index(drop=True)
        if limit:
            part = part.head(limit)
        print(f"{split}: {len(part)} vzoriek", flush=True)
        info[split] = build_split(part, out, split, ccfg) if len(part) else {"rows": 0}
        info[split]["missing_reports"] = int(((m["split"] == split) & missing).sum())
    files = sorted(out.glob("*.parquet"))
    write_json({"created": now_iso(), "script": "src/data/build_dynamic.py", "config_path": cfg_path, "config": ccfg,
                "splits": info, "complete": not missing.any() and not limit,
                "index_samples_sha256": sha256_file(INDEX_DIR / "samples.parquet"), "git": git_info(),
                "environment": environment(), "outputs": describe_files(files),
                "duration_s": round(time.perf_counter() - t0, 1)}, out / "manifest.json")
    print(f"Cache hotová: {rel(out)} ({time.perf_counter() - t0:.0f} s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", nargs="*", default=SPLIT_ORDER)
    ap.add_argument("--out", default=str(PROCESSED_DIR / "dynamic" / "cache"))
    ap.add_argument("--allow-missing", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--config", default="configs/data/dynamic.yaml")
    a = ap.parse_args()
    main(a.splits, Path(a.out), a.allow_missing, a.limit, a.config)
