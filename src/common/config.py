"""Načítanie YAML konfigurácií."""
from pathlib import Path

import yaml

from .paths import resolve


def load_config(path: str | Path) -> dict:
    with open(resolve(path), encoding="utf-8") as f:
        return yaml.safe_load(f)
