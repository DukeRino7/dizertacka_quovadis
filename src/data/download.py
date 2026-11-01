r"""Stiahnutie datasetu z Hugging Face do data/ (pôvodné dáta sa potom iba čítajú).

    .venv\Scripts\python.exe -m src.data.download --dataset ember
    .venv\Scripts\python.exe -m src.data.download --dataset speakeasy
Sťahuje sa revízia zafixovaná v konfigurácii (ember: configs/data/static.yaml -> ember_revision,
speakeasy: configs/data/dynamic.yaml -> speakeasy_revision; null = aktuálna). Už stiahnuté súbory sa preskočia,
takže prerušené sťahovanie sa dá spustiť znova. Záznam: processed/downloads/<dataset>.json (do data/ sa nezapisuje).
"""
import argparse

from huggingface_hub import HfApi, snapshot_download

from src.common.config import load_config
from src.common.paths import DATA_DIR, PROCESSED_DIR
from src.common.provenance import now_iso, write_json

DATASETS = {  # názov -> (repozitár, priečinok v data/, konfigurácia, kľúč revízie)
    "ember": ("dtrizna/quovadis-ember", "quovadis-ember", "configs/data/static.yaml", "ember_revision"),
    "speakeasy": ("dtrizna/quovadis-speakeasy", "quovadis-speakeasy", "configs/data/dynamic.yaml", "speakeasy_revision"),
}


def main(name: str):
    repo, folder, cfg_path, key = DATASETS[name]
    expected = load_config(cfg_path).get(key)
    latest = HfApi().dataset_info(repo).sha
    revision = expected or latest
    path = snapshot_download(repo_id=repo, repo_type="dataset", revision=revision, local_dir=DATA_DIR / folder, max_workers=8)
    write_json({"repo": repo, "revision": revision, "pinned_in_config": expected, "latest_on_hub": latest,
                "downloaded": now_iso(), "path": str(path)}, PROCESSED_DIR / "downloads" / f"{folder}.json")
    print(f"Stiahnuté: {repo} @ {revision} -> {path}")
    if not expected:
        print(f"Pozn.: revízia nie je zafixovaná – zapísať {key}: {revision} do {cfg_path}.")
    elif latest != expected:
        print(f"Pozn.: na Hugging Face je novšia revízia {latest}; projekt používa {expected}.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="ember", choices=sorted(DATASETS))
    main(ap.parse_args().dataset)
