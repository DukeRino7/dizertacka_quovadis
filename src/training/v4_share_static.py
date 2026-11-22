r"""V4 (docs/19, 4.2): statický model je vo vetvách real_p a emu_p ten istý.

Obe vetvy majú bitovo rovnaké statické dáta a rozdelenie (processed/kronodroid/{real_p,emu_p}/static). Statické
modely sa preto trénujú iba raz (real_p) a do emu_p sa skopírujú celé behy (model, predikcie, metriky, benchmark).
Skopírovaný beh dostane súbor SHARED_FROM.json. Pred kopírovaním sa overí zhoda dát (manifest SHA-256).

    .venv\Scripts\python.exe -m src.training.v4_share_static --src runs_v4/real_p/full --dst runs_v4/emu_p/full
"""
import argparse
import json
import shutil
from pathlib import Path

from src.common.paths import PROCESSED_DIR, PROJECT_ROOT, rel
from src.common.provenance import now_iso, write_json


def static_hashes(branch: str) -> dict:
    m = json.loads((PROCESSED_DIR / "kronodroid" / branch / "static" / "manifest.json").read_text(encoding="utf-8"))
    return {Path(o["path"]).name: o["sha256"] for o in m["outputs"]}


def main(src: Path, dst: Path) -> None:
    if static_hashes("real_p") != static_hashes("emu_p"):
        raise SystemExit("statické dáta real_p a emu_p sa líšia – zdieľanie statického modelu nie je prípustné")
    s, d = src / "static", dst / "static"
    if not s.exists() or not any((r / "metrics.json").exists() for m in s.iterdir() for r in m.iterdir() if r.is_dir()):
        raise SystemExit(f"v {rel(s)} nie sú dokončené statické behy")
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(s, d)
    for run in (r for m in d.iterdir() if m.is_dir() for r in m.iterdir() if (r / "metrics.json").exists()):
        write_json({"created": now_iso(), "copied_from": rel(src / "static" / run.parent.name / run.name),
                    "reason": "docs/19 4.2: statický model je v real_p a emu_p ten istý (rovnaké dáta, overené SHA-256)"},
                   run / "SHARED_FROM.json")
    print(f"statické behy skopírované: {rel(s)} -> {rel(d)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    a = ap.parse_args()
    main(PROJECT_ROOT / a.src, PROJECT_ROOT / a.dst)
