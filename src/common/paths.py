"""Cesty projektu na jednom mieste.

RUNS_DIR sa dá presmerovať premennou prostredia DIZERTACKA_RUNS_DIR (napr. finálny beh do samostatného priečinka).
"""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = PROJECT_ROOT / "processed"
RUNS_DIR = Path(os.environ.get("DIZERTACKA_RUNS_DIR") or PROJECT_ROOT / "runs").resolve()
CONFIGS_DIR = PROJECT_ROOT / "configs"

# Zero-day (docs/09): vynechaná rodina pre celý proces (nastavuje scripts/run_v2.ps1 pre každý beh).
# Ovplyvňuje src/data/providers.load_tabular: rodina sa odstráni z tréningu aj validácie, dynamické dáta sa berú
# zo slovníka bez nej a jej vzorky z tréningu a validácie tvoria časť 'holdout'.
HOLDOUT_FAMILY = os.environ.get("DIZERTACKA_HOLDOUT_FAMILY") or None
# Koreňe výsledkov, z ktorých sa preberajú hyperparametre (oddelené ';', poradie = priorita), napr. runs_v2/full;runs_final.
PARAMS_ROOTS = [Path(r) if Path(r).is_absolute() else PROJECT_ROOT / r
                for r in (os.environ.get("DIZERTACKA_PARAMS_ROOTS") or "").split(";") if r]

EMBER_DIR = DATA_DIR / "quovadis-ember"
SPEAKEASY_DIR = DATA_DIR / "quovadis-speakeasy"
INDEX_DIR = PROCESSED_DIR / "index"
STATIC_DIR = PROCESSED_DIR / "static"


def resolve(path: str | Path) -> Path:
    """Relatívnu cestu z konfigurácie vyhodnotí voči koreňu projektu."""
    p = Path(path)
    return p if p.is_absolute() else PROJECT_ROOT / p


def rel(path: Path) -> str:
    """Cesta relatívne ku koreňu projektu (na zápis do manifestov a reportov)."""
    try:
        return Path(path).resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path)
