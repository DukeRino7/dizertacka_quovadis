"""Priečinok jedného behu experimentu: runs/<prístup>/<model>/<dátum-čas>[_tag]/."""
import shutil
from datetime import datetime
from pathlib import Path

import yaml

from .paths import RUNS_DIR, resolve
from .provenance import environment, git_info, now_iso, write_json


def create_run_dir(approach: str, name: str, tag: str | None = None, runs_root: Path | None = None) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run = (runs_root or RUNS_DIR) / approach / name / (f"{stamp}_{tag}" if tag else stamp)
    run.mkdir(parents=True, exist_ok=False)
    for sub in ("model", "predictions", "plots"):
        (run / sub).mkdir()
    return run


def save_run_context(run: Path, config_path: str, config: dict, protocol: dict) -> None:
    shutil.copy(resolve(config_path), run / "config.yaml")
    with open(run / "protocol.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(protocol, f, allow_unicode=True, sort_keys=False)
    write_json({"created": now_iso(), "config_path": config_path, "git": git_info(), **environment()},
               run / "environment.json")
