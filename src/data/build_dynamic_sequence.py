r"""Postupnosti API volaní pre sekvenčné modely -> processed/dynamic/sequence/.

Token 0 = doplnenie (PAD), 1 = neznáme API (UNK), ďalej API zo slovníka naučeného IBA na tréningu
(min_freq dokumentovej frekvencie, najviac max_vocab). Vzorka = prvých max_len volaní celej postupnosti
(všetky vstupné body a vlákna v poradí reportu). Poradie vzoriek = spoločný index.

    .venv\Scripts\python.exe -m src.data.build_dynamic_sequence
Výstup: X_<časť>.npy (int32 [n, max_len]), y_<časť>.npy, meta_<časť>.parquet, vocab.json, manifest.json, README.md
"""
import argparse
import json
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from src.common.config import load_config
from src.common.paths import INDEX_DIR, PROCESSED_DIR, rel
from src.common.provenance import describe_files, environment, git_info, now_iso, write_json

SPLIT_ORDER = ["train", "validation", "test"]
PAD, UNK = 0, 1


def build_vocab(seqs, min_freq: int, max_vocab: int) -> dict[str, int]:
    df = Counter()
    for s in seqs:
        df.update(set(s))
    kept = sorted(((a, c) for a, c in df.items() if c >= min_freq), key=lambda x: (-x[1], x[0]))[:max_vocab]
    return {a: i + 2 for i, (a, _) in enumerate(kept)}


def encode(seqs, vocab: dict, max_len: int) -> tuple[np.ndarray, np.ndarray]:
    X = np.zeros((len(seqs), max_len), dtype=np.int32)
    lengths = np.zeros(len(seqs), dtype=np.int32)
    for i, s in enumerate(seqs):
        ids = [vocab.get(a, UNK) for a in s[:max_len]]
        X[i, :len(ids)] = ids
        lengths[i] = len(s)
    return X, lengths


def main(cache: Path, out: Path, cfg_path: str, exclude_family: str | None = None):
    t0 = time.perf_counter()
    scfg = load_config(cfg_path)["sequence"]
    out.mkdir(parents=True, exist_ok=True)
    index = pd.read_parquet(INDEX_DIR / "samples.parquet")
    data = {s: pd.read_parquet(cache / f"{s}.parquet", columns=["sha256", "family", "label", "api_seq"]) for s in SPLIT_ORDER}
    for s, d in data.items():
        ref = index.loc[index["split"] == s, "sha256"].to_numpy()
        if len(d) != len(ref) or not (d["sha256"].to_numpy() == ref).all():
            raise ValueError(f"{s}: cache nezodpovedá indexu – spustiť build_dynamic na kompletných dátach")
    tr = data["train"] if not exclude_family else data["train"][data["train"]["family"] != exclude_family]
    vocab = build_vocab(tr["api_seq"], scfg["min_freq"], scfg["max_vocab"])   # zero-day: bez vynechanej rodiny
    (out / "vocab.json").write_text(json.dumps({"PAD": PAD, "UNK": UNK, "tokens": vocab}, ensure_ascii=False), encoding="utf-8")
    stats, outputs = [], []
    for s, d in data.items():
        X, lengths = encode(d["api_seq"], vocab, scfg["max_len"])
        np.save(out / f"X_{s}.npy", X)
        np.save(out / f"y_{s}.npy", d["label"].to_numpy(np.int8))
        d[["sha256", "family", "label"]].to_parquet(out / f"meta_{s}.parquet", index=False)
        outputs += [out / f"X_{s}.npy", out / f"y_{s}.npy", out / f"meta_{s}.parquet"]
        nz = X[X > 0]
        stats.append({"časť": s, "vzorky": len(d), "orezané (> max_len)": round(float((lengths > scfg["max_len"]).mean()), 4),
                      "medián dĺžky": int(np.median(lengths)), "podiel UNK tokenov": round(float((nz == UNK).mean()) if nz.size else 0.0, 4)})
    st = pd.DataFrame(stats)
    write_json({"created": now_iso(), "script": "src/data/build_dynamic_sequence.py", "config": scfg,
                "exclude_family": exclude_family,
                "vocab_size": len(vocab) + 2, "stats": stats, "git": git_info(), "environment": environment(),
                "outputs": describe_files(outputs + [out / "vocab.json"]), "duration_s": time.perf_counter() - t0},
               out / "manifest.json")
    tbl = "| " + " | ".join(st.columns) + " |\n|" + "---|" * len(st.columns) + "\n" + "\n".join(
        "| " + " | ".join(str(v) for v in r) + " |" for r in st.itertuples(index=False))
    (out / "README.md").write_text(f"""# processed/dynamic/sequence/ – postupnosti API volaní pre sekvenčné modely

> Generované `src/data/build_dynamic_sequence.py` ({now_iso()}).

- Slovník z **tréningu**: {len(vocab)} API (min. {scfg['min_freq']} vzoriek, max. {scfg['max_vocab']}) + PAD (0) a UNK (1).
- Vzorka = prvých {scfg['max_len']} volaní celej postupnosti (všetky vstupné body a vlákna v poradí reportu), názvy malými písmenami.

{tbl}
""", encoding="utf-8")
    print(f"Sekvencie: {rel(out)}, slovník {len(vocab) + 2} ({time.perf_counter() - t0:.0f} s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=str(PROCESSED_DIR / "dynamic" / "cache"))
    ap.add_argument("--out", default=str(PROCESSED_DIR / "dynamic" / "sequence"))
    ap.add_argument("--config", default="configs/data/dynamic.yaml")
    ap.add_argument("--exclude-family", default=None, help="zero-day: slovník bez tejto rodiny -> processed/dynamic/lofo/<rodina>/sequence")
    a = ap.parse_args()
    out = Path(a.out)
    if a.exclude_family and a.out == str(PROCESSED_DIR / "dynamic" / "sequence"):
        out = PROCESSED_DIR / "dynamic" / "lofo" / a.exclude_family / "sequence"
    main(Path(a.cache), out, a.config, a.exclude_family)
