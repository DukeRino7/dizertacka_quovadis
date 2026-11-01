"""Meranie výpočtových nárokov inferencie.

- latencia jednej vzorky (batch = 1) na CPU s pevným počtom vlákien – medián a 95. percentil,
- priepustnosť na celej množine (dávkovo) na CPU so všetkými vláknami,
- pri modeloch v PyTorch aj GPU (latencia aj priepustnosť).
Čas prípravy vstupu (učená transformácia) sa meria oddelene od modelu.
"""
import time
from typing import Callable

import numpy as np
from threadpoolctl import threadpool_limits


def _sync(device: str | None):
    if device == "cuda":
        import torch
        torch.cuda.synchronize()


def latency(predict: Callable, X: np.ndarray, n: int, warmup: int, seed: int = 0, device: str | None = None) -> dict:
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(X), min(n, len(X)), replace=False)
    rows = [np.ascontiguousarray(X[i:i + 1]) for i in idx]
    for r in rows[:warmup]:
        predict(r)
    times = []
    for r in rows:
        _sync(device)
        t = time.perf_counter()
        predict(r)
        _sync(device)
        times.append(time.perf_counter() - t)
    t = np.array(times) * 1e3
    return {"n": len(rows), "median_ms": float(np.median(t)), "p95_ms": float(np.percentile(t, 95)),
            "mean_ms": float(t.mean())}


def throughput(predict: Callable, X: np.ndarray, device: str | None = None) -> dict:
    predict(np.ascontiguousarray(X[:256]))  # zahriatie
    _sync(device)
    t = time.perf_counter()
    predict(X)
    _sync(device)
    dt = time.perf_counter() - t
    return {"n": int(len(X)), "total_s": dt, "samples_per_s": len(X) / dt, "us_per_sample": dt / len(X) * 1e6}


def measure_inference(model, transform: Callable | None, X_raw: np.ndarray, cfg: dict) -> dict:
    """Model musí mať predict_proba(X) a set_threads(n); voliteľne to_device(dev) a supports_gpu."""
    out = {}
    X = np.ascontiguousarray(X_raw)
    if transform is not None:
        with threadpool_limits(cfg["latency_threads"]):
            out["transform_cpu_latency"] = latency(transform, X, cfg["latency_samples"], cfg["warmup"])
        with threadpool_limits(cfg["throughput_threads"]):
            out["transform_cpu_throughput"] = throughput(transform, X)
        X = transform(X)

    model.set_threads(cfg["latency_threads"])
    with threadpool_limits(cfg["latency_threads"]):
        out["cpu_latency"] = latency(model.predict_proba, X, cfg["latency_samples"], cfg["warmup"])
    model.set_threads(cfg["throughput_threads"])
    with threadpool_limits(cfg["throughput_threads"]):
        out["cpu_throughput"] = throughput(model.predict_proba, X)

    if cfg.get("gpu") and getattr(model, "supports_gpu", False):
        import torch
        if torch.cuda.is_available():
            model.to_device("cuda")
            torch.cuda.reset_peak_memory_stats()
            out["gpu_latency"] = latency(model.predict_proba, X, cfg["latency_samples"], cfg["warmup"], device="cuda")
            out["gpu_throughput"] = throughput(model.predict_proba, X, device="cuda")
            out["gpu_peak_memory_mb"] = torch.cuda.max_memory_allocated() / 1e6
            model.to_device("cpu")
    return out
