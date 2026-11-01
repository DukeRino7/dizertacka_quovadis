"""Spustí všetky kontrolné experimenty z configs/<priečinok>/ a vytvorí ich porovnanie.

    .venv\Scripts\python.exe -m src.training.run_ablations --dir static_ablations
"""
import argparse
import traceback

from src.common.paths import CONFIGS_DIR
from src.evaluation.compare_ablations import main as compare
from .run_tabular import main as run_one

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="static_ablations")
    a = ap.parse_args()
    for cfg in sorted((CONFIGS_DIR / a.dir).glob("*.yaml")):
        try:
            run_one(f"configs/{a.dir}/{cfg.name}", None, None, False)
        except Exception:
            print(f"!!! {cfg.name} zlyhal:\n{traceback.format_exc()}", flush=True)
    compare(a.dir)
