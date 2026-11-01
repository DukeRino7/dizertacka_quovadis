"""Cesty projektu na jednom mieste."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = PROJECT_ROOT / "processed"
RUNS_DIR = PROJECT_ROOT / "runs"
CONFIGS_DIR = PROJECT_ROOT / "configs"

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
