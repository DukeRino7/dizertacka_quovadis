"""Centrálny register všetkých modelov (hodnota `model:` v konfigurácii -> trieda)."""
from src.models.tabular import REGISTRY as _TABULAR


def _extra():
    from src.models.dynamic.sequence_cnn import SequenceCNN
    from src.models.hybrid.two_branch import TwoBranchHybrid
    return {m.name: m for m in (SequenceCNN, TwoBranchHybrid)}


def get_model_class(name: str):
    reg = {**_TABULAR, **_extra()}
    if name not in reg:
        raise KeyError(f"neznámy model {name!r}; dostupné: {sorted(reg)}")
    return reg[name]
