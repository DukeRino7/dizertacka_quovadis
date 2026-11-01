"""Jednotné meranie výpočtových nárokov inferencie z uložených modelov.

Rovnaký postup pre všetky prístupy (static, dynamic, hybrid, kaskáda), aby sa dali povedať vety typu
„kaskáda spotrebuje menej výpočtového výkonu než hybridný model“. Meria sa celá cesta
pôvodný vstup -> transformácia -> model -> skóre na testovacej množine.

Scenáre:
- cpu_batch  – dávková inferencia na CPU, všetky vlákna (priepustnosť, CPU čas, vyťaženie CPU, RAM)
- cpu_single – jedna vzorka naraz, 1 vlákno (latencia, CPU čas na vzorku)
- gpu_batch / gpu_single – to isté s modelom na GPU (iba modely v PyTorch)

Spúšťať na NEZAŤAŽENOM počítači (bez tréningu a sťahovania); zaťaženie pred meraním sa zapisuje.
    .venv\\Scripts\\python.exe -m src.evaluation.benchmark --approach static
"""
import argparse
import json
import time
from pathlib import Path

import joblib
import numpy as np
import psutil
from threadpoolctl import threadpool_limits

from src.common.config import load_config
from src.common.paths import RUNS_DIR, rel
from src.common.provenance import environment, now_iso, write_json
from src.data.providers import load_tabular
from src.models.registry import get_model_class
from .compare import latest_runs
from .resources import ResourceMonitor, gpu_idle_power_w


def make_pipeline(run: Path, model_name: str):
    pre_path = run / "model" / "preprocessor.joblib"
    pre = joblib.load(pre_path) if pre_path.exists() else None
    model = get_model_class(model_name).load(run / "model" / "seed_0")
    mask_path = run / "model" / "feature_mask.json"
    cols = np.array(json.loads(mask_path.read_text())["kept_columns"]) if mask_path.exists() else None

    def predict(X):
        if cols is not None:
            X = X[:, cols]
        return model.predict_proba(pre.transform(X) if pre is not None else X)
    return model, predict


def _batch(predict, X, min_seconds: float, gpu: bool, idle_w):
    predict(X[:256])  # zahriatie
    reps, n = 0, 0
    with ResourceMonitor(gpu=gpu) as mon:
        start = time.perf_counter()
        while reps == 0 or time.perf_counter() - start < min_seconds:
            predict(X); reps += 1; n += len(X)
            if gpu:
                import torch; torch.cuda.synchronize()
    return {**mon.result(n, idle_w), "repetitions": reps}


def _single(predict, X, n: int, warmup: int, gpu: bool, idle_w, min_seconds: float, seed: int = 0):
    """Vzorky po jednej; zoznam n vzoriek sa prechádza opakovane, kým neuplynie min_seconds
    (CPU čas z OS má na Windows rozlíšenie ~15 ms, krátke meranie by bolo nepresné)."""
    rng = np.random.default_rng(seed)
    rows = [np.ascontiguousarray(X[i:i + 1]) for i in rng.choice(len(X), min(n, len(X)), replace=False)]
    for r in rows[:warmup]:
        predict(r)
    times = []
    with ResourceMonitor(gpu=gpu) as mon:
        start = time.perf_counter()
        while not times or time.perf_counter() - start < min_seconds:
            for r in rows:
                t = time.perf_counter()
                predict(r)
                if gpu:
                    import torch; torch.cuda.synchronize()
                times.append(time.perf_counter() - t)
    t = np.array(times) * 1e3
    return {**mon.result(len(times), idle_w), "latency_median_ms": float(np.median(t)),
            "latency_p95_ms": float(np.percentile(t, 95))}


def benchmark_run(run: Path, model_name: str, X: np.ndarray, cfg: dict) -> dict:
    model, predict = make_pipeline(run, model_name)
    load_before = psutil.cpu_percent(interval=1.0)
    out = {"created": now_iso(), "run": rel(run), "n_test": int(len(X)),
           "system_cpu_load_before_pct": load_before, "config": cfg}

    model.set_threads(cfg["batch_threads"])
    with threadpool_limits(cfg["batch_threads"]):
        out["cpu_batch"] = _batch(predict, X, cfg["min_seconds"], False, None)
    model.set_threads(1)
    with threadpool_limits(1):
        out["cpu_single"] = _single(predict, X, cfg["single_samples"], cfg["warmup"], False, None, cfg["min_seconds"])

    if getattr(model, "supports_gpu", False) and cfg.get("gpu", True):
        import torch
        if torch.cuda.is_available():
            idle = gpu_idle_power_w()
            out["gpu_idle_power_w"] = idle
            model.to_device("cuda")
            model.set_threads(cfg["batch_threads"])
            with threadpool_limits(cfg["batch_threads"]):
                out["gpu_batch"] = _batch(predict, X, cfg["min_seconds"], True, idle)
                out["gpu_single"] = _single(predict, X, cfg["single_samples"], cfg["warmup"], True, idle, cfg["min_seconds"])
            model.to_device("cpu")
    if load_before > cfg["max_background_load_pct"]:
        out["warning"] = f"systém bol pred meraním zaťažený na {load_before:.0f} % – výsledky môžu byť skreslené"
    return out


def main(approach: str, models: list[str] | None):
    protocol = load_config("configs/protocol.yaml")
    cfg = protocol["benchmark"]
    cache = {}
    for name, run in latest_runs(approach).items():
        if models and name not in models:
            continue
        rcfg = load_config(run / "config.yaml")
        model_name, data_approach = rcfg["model"], rcfg["approach"]   # napr. seq_cnn číta 'dynamic_seq'
        if data_approach not in cache:
            cache.clear()
            cache[data_approach] = np.ascontiguousarray(load_tabular(data_approach, splits=("test",))["test"][0])
        X = cache[data_approach]
        print(f"{approach}/{name}: meranie ...", flush=True)
        res = benchmark_run(run, model_name, X, cfg)
        res["environment"] = environment()
        write_json(res, run / "benchmark.json")
        cb, cs = res["cpu_batch"], res["cpu_single"]
        print(f"  CPU dávka: {cb['samples_per_s']:,.0f} vz/s, {cb['cpu_ms_per_sample']:.3f} ms CPU/vz, "
              f"vyťaženie {cb['cpu_util_pct']:.0f} % | 1 vzorka: {cs['latency_median_ms']:.3f} ms"
              + (f" | {res['warning']}" if "warning" in res else ""), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--approach", default="static")
    ap.add_argument("--models", nargs="*", default=None)
    a = ap.parse_args()
    main(a.approach, a.models)
