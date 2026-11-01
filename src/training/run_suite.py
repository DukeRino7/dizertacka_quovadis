r"""Spustí sadu modelov jedného prístupu za sebou a na konci vytvorí porovnanie.

    .venv\Scripts\python.exe -m src.training.run_suite --approach static
    .venv\Scripts\python.exe -m src.training.run_suite --approach dynamic --models lr rf lightgbm mlp_small mlp_large seq_cnn
    .venv\Scripts\python.exe -m src.training.run_suite --approach static --skip-done   # pokračovanie po prerušení

Konfigurácia modelu = configs/<prístup>/<model>.yaml. --skip-done preskočí model, ktorý už má dokončený beh
v aktuálnom priečinku výsledkov (RUNS_DIR).
"""
import argparse
import traceback

from src.common.config import load_config
from src.common.paths import CONFIGS_DIR, RUNS_DIR
from src.evaluation.compare import main as compare
from .run_tabular import main as run_one

LADDER = ["lr", "rf", "lightgbm", "mlp_small", "mlp_large"]


def is_done(config_path: str) -> bool:
    cfg = load_config(config_path)
    d = RUNS_DIR / cfg.get("results_approach", cfg["approach"]) / cfg["name"]
    return d.exists() and any((r / "metrics.json").exists() for r in d.iterdir() if r.is_dir())


def run_configs(configs: list[str], skip_done: bool) -> list[str]:
    failed = []
    for c in configs:
        if skip_done and is_done(c):
            print(f"--- {c}: už dokončené, preskakujem", flush=True)
            continue
        try:
            run_one(c, None, None, False)
        except Exception:
            print(f"!!! {c} zlyhal:\n{traceback.format_exc()}", flush=True)
            failed.append(c)
    return failed


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--approach", default="static")
    ap.add_argument("--models", nargs="*", default=LADDER)
    ap.add_argument("--skip-done", action="store_true")
    ap.add_argument("--no-compare", action="store_true")
    a = ap.parse_args()
    failed = run_configs([f"configs/{a.approach}/{m}.yaml" for m in a.models], a.skip_done)
    if not a.no_compare:
        compare(a.approach)
    if failed:
        raise SystemExit(f"zlyhali: {failed}")
