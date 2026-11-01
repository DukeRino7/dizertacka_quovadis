"""Zoznam Speakeasy reportov podľa SHA-256.

Kým nie je Speakeasy dataset celý stiahnutý, existencia reportov sa overuje zo zoznamu súborov
repozitára na Hugging Face (cache `huggingface_hub`, obsahuje cesty a veľkosti všetkých súborov).
Overené v audite: train `<sha>.json`, test `<sha>.dat.json`, train backdoor/clean o úroveň hlbšie;
`report_windows_syswow64` je pomenovaný podľa programu (nie SHA-256) a nedá sa spárovať.
"""
import json
import re
from pathlib import Path

import pandas as pd

_SHA = re.compile(r"^[0-9a-f]{64}$")


def family_from_folder(folder: str) -> str:
    name = folder.removeprefix("report_")
    return "benign" if name in ("clean", "windows_syswow64") else name


def read_listing(tree_json: Path) -> pd.DataFrame:
    """Vráti sha256, original_split, family, speakeasy_path (relatívne k data/quovadis-speakeasy), speakeasy_bytes."""
    with open(tree_json, encoding="utf-8") as f:
        files = json.load(f)["files"]
    rows = []
    for path, meta in files.items():
        parts = path.split("/")
        if len(parts) not in (3, 4) or not parts[0].startswith("windows_emulation_"):
            continue
        sha = parts[-1].split(".")[0]
        if not _SHA.match(sha) or not parts[-1].endswith(".json"):
            continue
        split = "train" if parts[0].endswith("trainset") else "test"
        rows.append((sha, split, family_from_folder(parts[1]), path, int(meta["size"])))
    return pd.DataFrame(rows, columns=["sha256", "original_split", "family", "speakeasy_path", "speakeasy_bytes"])
