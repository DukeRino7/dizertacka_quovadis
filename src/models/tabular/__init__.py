"""Spoločný rebríček modelov nad pevným vektorom príznakov (static / dynamic / hybrid)."""
from .lightgbm_model import LightGBM
from .logreg import LogReg
from .mlp import MLP
from .random_forest import RandomForest

REGISTRY = {m.name: m for m in (LogReg, RandomForest, LightGBM, MLP)}


def get_model_class(name: str):
    if name not in REGISTRY:
        raise KeyError(f"neznámy model {name!r}; dostupné: {sorted(REGISTRY)}")
    return REGISTRY[name]
