"""Záznam pôvodu výstupov: verzia kódu, prostredie, kontrolné súčty súborov."""
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

from .paths import PROJECT_ROOT, rel

_PACKAGES = ["numpy", "pandas", "pyarrow", "scikit-learn", "scipy", "matplotlib", "torch", "lightgbm", "xgboost"]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def git_info() -> dict:
    def run(*args):
        try:
            return subprocess.run(["git", *args], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True).stdout.strip()
        except Exception:
            return None
    status = run("status", "--porcelain")
    return {"commit": run("rev-parse", "HEAD"), "dirty": bool(status) if status is not None else None}


def environment() -> dict:
    versions = {}
    for p in _PACKAGES:
        try:
            versions[p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            pass
    out = {"python": sys.version.split()[0], "platform": platform.platform(), "machine": platform.node(),
           "processor": platform.processor(), "packages": versions}
    try:
        import psutil
        out["cpu_physical"], out["cpu_logical"] = psutil.cpu_count(logical=False), psutil.cpu_count()
        out["ram_gb"] = round(psutil.virtual_memory().total / 1e9, 1)
    except ImportError:
        pass
    try:
        import torch
        out["gpu"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    except Exception:
        out["gpu"] = None
    return out


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def describe_files(paths: list[Path]) -> list[dict]:
    return [{"path": rel(p), "bytes": p.stat().st_size, "sha256": sha256_file(p)} for p in paths]


def write_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, default=str)
