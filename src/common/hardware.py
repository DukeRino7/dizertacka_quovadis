"""Prispôsobenie počtu vlákien hardvéru (aby sa ten istý protokol dal spustiť na inom počítači).

V configs/protocol.yaml: auto_threads: true ->
- tréning (training_threads) = počet FYZICKÝCH jadier (odporúčanie LightGBM; hyperthreading tréning spomaľuje),
- priepustnosť a benchmark dávky = počet LOGICKÝCH jadier,
- latencia jednej vzorky ostáva 1 vlákno (porovnateľné medzi modelmi).
Skutočne použité hodnoty sa ukladajú do protocol.yaml v priečinku behu.
"""
import os

import psutil

from .config import load_config


def cpu_counts() -> tuple[int, int]:
    return psutil.cpu_count(logical=False) or os.cpu_count() or 1, os.cpu_count() or 1


def load_protocol(path: str = "configs/protocol.yaml") -> dict:
    p = load_config(path)
    if p.get("auto_threads"):
        physical, logical = cpu_counts()
        p["training_threads"] = physical
        p["timing"]["throughput_threads"] = logical
        if "benchmark" in p:
            p["benchmark"]["batch_threads"] = logical
    p.setdefault("training_threads", p["timing"]["throughput_threads"])
    return p
