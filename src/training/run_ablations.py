r"""Spustí všetky kontrolné experimenty z configs/<priečinok>/ a vytvorí ich porovnanie.

    .venv\Scripts\python.exe -m src.training.run_ablations --dir static_ablations
"""
import argparse

from src.common.paths import CONFIGS_DIR
from src.evaluation.compare_ablations import main as compare

if __name__ == "__main__":
    from .run_suite import run_configs
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="static_ablations")
    ap.add_argument("--skip-done", action="store_true", help="preskočiť ablácie s dokončeným behom")
    a = ap.parse_args()
    failed = run_configs([f"configs/{a.dir}/{c.name}" for c in sorted((CONFIGS_DIR / a.dir).glob("*.yaml"))], a.skip_done)
    compare(a.dir)
    if failed:
        raise SystemExit(f"zlyhali: {failed}")
