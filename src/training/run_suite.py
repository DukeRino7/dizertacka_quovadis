"""Spustí rebríček modelov jedného prístupu za sebou a na konci vytvorí porovnanie.

    .venv\Scripts\python.exe -m src.training.run_suite --approach static
    .venv\Scripts\python.exe -m src.training.run_suite --approach static --models lr lightgbm
"""
import argparse
import traceback

from src.common.paths import CONFIGS_DIR
from src.evaluation.compare import main as compare
from .run_tabular import main as run_one

LADDER = ["lr", "rf", "lightgbm", "mlp_small", "mlp_large"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--approach", default="static")
    ap.add_argument("--models", nargs="*", default=LADDER)
    a = ap.parse_args()
    for name in a.models:
        try:
            run_one(f"configs/{a.approach}/{name}.yaml", None, None, False)
        except Exception:
            print(f"!!! {name} zlyhal:\n{traceback.format_exc()}", flush=True)
    compare(a.approach)
