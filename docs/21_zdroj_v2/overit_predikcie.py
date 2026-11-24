"""Kontrolné výpočty zo súborov predikcií. Spúšťať z koreňa repozitára cez Python -B."""
import json
import sys
from pathlib import Path

import numpy as np

OUTPUT = Path(__file__).resolve().parent
ROOT = OUTPUT.parents[1]
sys.path.insert(0, str(ROOT))

from src.cascade.components import Component
from src.common.config import load_config
from src.evaluation import metrics
from src.evaluation.v4_report import (
    Boot, CASCADES, Setting, main_metrics, tpr_at_fpr_w, zero_day_metrics,
)

QV_FAMILIES = ("backdoor", "coinminer", "dropper", "keylogger", "ransomware", "rat", "trojan")
MODELS = ("static", "dynamic", "hybrid")


def qv_at_roc(path, family=None, with_holdout=False):
    result = {}
    for model in MODELS:
        component = Component(f"{model}/lightgbm", path)
        scores = []
        for seed in component.seeds:
            test = component.scores("test", seed)
            benign = test.loc[test["label"] == 0, "score"].to_numpy()
            mask = (test["label"] == 1)
            if family:
                mask &= test["family"].eq(family)
            malware = test.loc[mask, "score"].to_numpy()
            if with_holdout:
                held = component.scores("holdout", seed)
                assert held["family"].eq(family).all()
                malware = np.concatenate([malware, held["score"].to_numpy()])
            scores.append(float(tpr_at_fpr_w(
                benign, malware, np.ones((1, len(benign))), np.ones((1, len(malware)))
            )[0]))
        result[model] = float(np.mean(scores))
    return result


def qv_zero(with_holdout=False):
    families = {
        family: qv_at_roc(ROOT / "runs_v2" / "lofo" / family, family, with_holdout)
        for family in QV_FAMILIES
    }
    return {
        "families": families,
        "mean": {key: float(np.mean([row[key] for row in families.values()])) for key in MODELS},
    }


def android(branch, families):
    base = ROOT / "runs_v4" / branch
    full = Setting(base / "full")
    full_data = [full.seed_data(seed) for seed in full.seeds]
    main = main_metrics(full, full_data, Boot(full.meta["label"].to_numpy(), 1))
    settings = [Setting(base / "lofo" / f.replace("/", "_").replace(" ", "_"), f) for f in families]
    data = [[s.seed_data(seed) for seed in s.seeds] for s in settings]
    zero = zero_day_metrics(settings, data, 1)
    assert zero["families"] == families

    # TPR všetkého malvéru podľa docs/09 sa určuje len na bežnej časti testu.
    # Doplnkovo zostáva TPR vynechanej rodiny (test aj odložená časť) zo súhrnu V4.
    all_test = {}
    for key in ("static", "dynamic", *CASCADES):
        all_test[key] = []
        for setting, D in zip(settings, data):
            labels = setting.meta["label"].to_numpy()
            all_test[key].append(np.mean([
                metrics.at_threshold(labels, d["dec"]["test"][key], 0.5)["recall_tpr"] for d in D
            ]))

    z = zero["avg"]["dec"]
    averages = {key: {
        "family_tpr": float(z[key]["tpr"][0]),
        "all_test_malware_tpr": float(np.mean(all_test[key])),
        "fpr": float(z[key]["fpr"][0]),
        "family_std": float(np.std([
            zero["per_family"][f]["dec"][key]["tpr"][0] for f in families
        ], ddof=1)),
        "main_tpr": float(main["dec"][key]["tpr"][0]),
        "main_fpr": float(main["dec"][key]["fpr"][0]),
        "main_rate": main["rates"].get(key),
        "zero_test_rate": zero["avg"]["rates"].get(key),
    } for key in ("static", "dynamic", *CASCADES)}

    def meets_t2(row, tpr_key, fpr_key):
        return (
            row[fpr_key] < min(averages["static"][fpr_key], averages["dynamic"][fpr_key])
            and row[tpr_key] >= averages["static"][tpr_key] - 0.01
        )

    for key in CASCADES:
        row = averages[key]
        row["t2_main"] = meets_t2(row, "main_tpr", "main_fpr")
        row["t2_zero_family"] = meets_t2(row, "family_tpr", "fpr")
        row["t2_zero_all_test"] = meets_t2(row, "all_test_malware_tpr", "fpr")
    for key in ("static", "dynamic", "A_baselines", "B_baselines_10"):
        row = averages[key]
        row["alarms_at_01_percent"] = metrics.at_prevalence(
            row["main_tpr"], row["main_fpr"], 0.001
        )["false_per_true_alarm"]
    return {
        "decision": averages,
        "zero_roc": {key: float(zero["avg"]["roc"][key][0]) for key in MODELS},
    }


def main():
    families = load_config(ROOT / "configs/kronodroid/data.yaml")["v4"]["holdout_families"]
    checks = {
        "qv_main_roc": qv_at_roc(ROOT / "runs_final"),
        "qv_zero_test_roc": qv_zero(),
        "qv_zero_with_holdout_roc": qv_zero(with_holdout=True),
        "kronodroid": {branch: android(branch, families) for branch in ("real_full", "real_p", "emu_p")},
    }
    output = OUTPUT / "overene_hodnoty.json"
    output.write_text(json.dumps(checks, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()

