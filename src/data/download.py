"""Stiahnutie datasetu z Hugging Face do data/ (pôvodné dáta sa potom iba čítajú).

    .venv\Scripts\python.exe -m src.data.download --dataset ember
Revízia sa overí voči configs/data/static.yaml (ember_revision) a zapíše do processed/downloads/<dataset>.json
(do data/ sa nič nezapisuje).
"""
import argparse

from huggingface_hub import HfApi, snapshot_download

from src.common.config import load_config
from src.common.paths import DATA_DIR, PROCESSED_DIR
from src.common.provenance import now_iso, write_json

DATASETS = {"ember": ("dtrizna/quovadis-ember", "quovadis-ember")}


def main(name: str):
    repo, folder = DATASETS[name]
    expected = load_config("configs/data/static.yaml").get("ember_revision")
    # sťahuje sa presne revízia použitá v projekte (nie najnovšia), aby mali všetky počítače rovnaké dáta
    path = snapshot_download(repo_id=repo, repo_type="dataset", revision=expected, local_dir=DATA_DIR / folder, max_workers=8)
    latest = HfApi().dataset_info(repo).sha
    write_json({"repo": repo, "revision": expected, "latest_on_hub": latest, "downloaded": now_iso(), "path": str(path)},
               PROCESSED_DIR / "downloads" / f"{folder}.json")
    print(f"Stiahnuté: {repo} @ {expected} -> {path}")
    if latest != expected:
        print(f"Pozn.: na Hugging Face je novšia revízia {latest}; projekt používa {expected}.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="ember", choices=sorted(DATASETS))
    main(ap.parse_args().dataset)
