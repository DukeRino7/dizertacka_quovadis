"""Načítanie uložených predikcií, prahov a nárokov komponentov kaskády / fúzie.

Komponent sa zadáva ako '<prístup>/<model>' (posledný dokončený beh v runs/) alebo cesta k behu.
"""
import json
import os
from pathlib import Path

import pandas as pd

from src.common.paths import PROJECT_ROOT, RUNS_DIR


def resolve_run(spec: str, runs_root: Path = RUNS_DIR) -> Path:
    from src.training.select_best import resolve_auto  # 'auto:hybrid' -> vybraný model podľa pravidla
    spec = resolve_auto(spec)
    p = Path(spec)
    if not p.is_absolute():
        cand = PROJECT_ROOT / spec
        if (cand / "metrics.json").exists():
            return cand
        # DIZERTACKA_RESULTS_FALLBACK: ďalšie koreňe výsledkov (oddelené ';'), napr. runs_final pre kaskády B na modeloch V1
        roots = [runs_root] + [PROJECT_ROOT / r for r in os.environ.get("DIZERTACKA_RESULTS_FALLBACK", "").split(";") if r]
        for root in roots:
            base = root / spec
            runs = sorted(r for r in base.iterdir() if (r / "metrics.json").exists()) if base.exists() else []
            if runs:
                return runs[-1]
        raise FileNotFoundError(f"komponent {spec!r}: žiadny dokončený beh v {[str(r) for r in roots]}")
    return p


class Component:
    def __init__(self, spec: str, runs_root: Path = RUNS_DIR):
        self.spec = spec
        self.run = resolve_run(spec, runs_root)
        self.metrics = json.loads((self.run / "metrics.json").read_text(encoding="utf-8"))
        self.seeds = self.metrics["seeds"]
        b = self.run / "benchmark.json"
        self.benchmark = json.loads(b.read_text(encoding="utf-8")) if b.exists() else None

    def threshold(self, seed: int, kind: str = "val_fpr") -> float:
        r = next(r for r in self.metrics["per_seed"] if r["seed"] == seed)
        return float(r["thresholds"][kind])

    def has_split(self, split: str, seed: int) -> bool:
        return (self.run / "predictions" / f"{split}_seed{seed}.parquet").exists()

    def scores(self, split: str, seed: int) -> pd.DataFrame:
        return pd.read_parquet(self.run / "predictions" / f"{split}_seed{seed}.parquet")

    def cost(self) -> dict | None:
        """CPU čas na vzorku [ms] a latencia [ms] z benchmarku (ak bol spustený)."""
        if not self.benchmark:
            return None
        b = self.benchmark
        out = {"cpu_ms_batch": b["cpu_batch"]["cpu_ms_per_sample"], "cpu_ms_single": b["cpu_single"]["cpu_ms_per_sample"],
               "latency_ms": b["cpu_single"]["latency_median_ms"]}
        if "gpu_batch" in b:
            out["gpu_j_per_1000"] = b["gpu_batch"].get("gpu_energy_above_idle_j_per_1000")
        return out
