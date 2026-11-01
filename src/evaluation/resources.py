"""Meranie spotreby výpočtových zdrojov počas inferencie.

Monitor počas behu zaznamená:
- CPU čas procesu (user + system) – koľko „jadro-sekúnd“ výpočet spotreboval (presné, z OS),
- priemerné vyťaženie CPU = CPU čas / (čas behu × počet logických jadier),
- maximálnu RAM procesu (vzorkovanie každých 50 ms) a jej nárast oproti začiatku,
- pri GPU: priemerné vyťaženie (NVML, vzorkovanie), maximálnu alokovanú pamäť (PyTorch),
  energiu z hardvérového počítadla karty a energiu nad úrovňou nečinnosti (idle).
Spotrebu energie CPU na Windows nevieme spoľahlivo zmerať, preto sa neuvádza.
"""
import os
import threading
import time

import psutil

try:
    import pynvml
    pynvml.nvmlInit()
    _GPU = pynvml.nvmlDeviceGetHandleByIndex(0)
except Exception:  # bez NVIDIA GPU / ovládača
    _GPU = None

N_LOGICAL = os.cpu_count() or 1


def gpu_idle_power_w(seconds: float = 2.0) -> float | None:
    """Priemerný príkon karty v nečinnosti (na odpočet od energie počas inferencie)."""
    if _GPU is None:
        return None
    vals, end = [], time.perf_counter() + seconds
    while time.perf_counter() < end:
        vals.append(pynvml.nvmlDeviceGetPowerUsage(_GPU) / 1000)
        time.sleep(0.05)
    return sum(vals) / len(vals)


class ResourceMonitor:
    def __init__(self, gpu: bool = False, interval: float = 0.05):
        self.proc = psutil.Process()
        self.gpu = gpu and _GPU is not None
        self.interval = interval

    def _sample(self):
        while not self._stop.is_set():
            self.peak_rss = max(self.peak_rss, self.proc.memory_info().rss)
            if self.gpu:
                self.gpu_util.append(pynvml.nvmlDeviceGetUtilizationRates(_GPU).gpu)
            time.sleep(self.interval)

    def __enter__(self):
        self.rss0 = self.peak_rss = self.proc.memory_info().rss
        self.gpu_util = []
        if self.gpu:
            import torch
            torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
            self.energy0 = pynvml.nvmlDeviceGetTotalEnergyConsumption(_GPU)
        self.cpu0 = self.proc.cpu_times()
        self.t0 = time.perf_counter()
        self._stop = threading.Event()
        self._thr = threading.Thread(target=self._sample, daemon=True)
        self._thr.start()
        return self

    def __exit__(self, *exc):
        if self.gpu:
            import torch
            torch.cuda.synchronize()
        self.wall = time.perf_counter() - self.t0
        cpu1 = self.proc.cpu_times()
        self._stop.set(); self._thr.join()
        self.cpu_s = (cpu1.user - self.cpu0.user) + (cpu1.system - self.cpu0.system)
        if self.gpu:
            import torch
            self.energy_j = (pynvml.nvmlDeviceGetTotalEnergyConsumption(_GPU) - self.energy0) / 1000
            self.gpu_mem_mb = torch.cuda.max_memory_allocated() / 1e6
        return False

    def result(self, n_samples: int, idle_w: float | None = None) -> dict:
        out = {
            "n_samples": n_samples, "wall_s": self.wall,
            "samples_per_s": n_samples / self.wall,
            "latency_ms_per_sample": self.wall / n_samples * 1e3,
            "cpu_ms_per_sample": self.cpu_s / n_samples * 1e3,
            "cpu_util_pct": 100 * self.cpu_s / (self.wall * N_LOGICAL),
            "cores_busy": self.cpu_s / self.wall,
            "ram_peak_mb": self.peak_rss / 1e6,
            "ram_increase_mb": (self.peak_rss - self.rss0) / 1e6,
        }
        if self.gpu:
            out.update({
                "gpu_util_pct": sum(self.gpu_util) / max(len(self.gpu_util), 1),
                "gpu_mem_peak_mb": self.gpu_mem_mb,
                "gpu_energy_j_per_1000": self.energy_j / n_samples * 1000,
            })
            if idle_w is not None:
                out["gpu_energy_above_idle_j_per_1000"] = max(self.energy_j - idle_w * self.wall, 0) / n_samples * 1000
        return out
