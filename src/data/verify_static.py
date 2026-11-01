r"""Overenie skopírovaných statických dát voči kontrolným súčtom v gite (processed/static/manifest.json).

    .venv\Scripts\python.exe -m src.data.verify_static
"""
import json
import sys

from src.common.paths import PROJECT_ROOT, STATIC_DIR
from src.common.provenance import sha256_file

if __name__ == "__main__":
    ref = json.loads((STATIC_DIR / "manifest.json").read_text(encoding="utf-8"))["outputs"]
    bad = []
    for o in ref:
        if any(k in o["path"] for k in ("/X_", "/y_", "/meta_")):
            p = PROJECT_ROOT / o["path"]
            ok = p.exists() and sha256_file(p) == o["sha256"]
            print(("OK      " if ok else "CHYBA   ") + o["path"])
            bad += [] if ok else [o["path"]]
    print("ZHODA – dáta sú identické s gitom" if not bad else f"NEZHODA: {bad}")
    sys.exit(1 if bad else 0)
