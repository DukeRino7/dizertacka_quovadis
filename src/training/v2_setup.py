r"""Príprava priečinka zero-day behu (docs/09): pevný výber architektúr z V1.

Vo V2 sa výber modelov neopakuje – v každom behu sa použijú rovnaké architektúry ako vo V1, aby boli behy
porovnateľné. Zapíše <RUNS_DIR>/selection/{static,dynamic,hybrid}.json s kľúčom 'chosen' prevzatým z V1
(rovnaký formát ako src.training.select_best, 'auto:<skupina>' potom funguje bez zmeny).

    .venv\Scripts\python.exe -m src.training.v2_setup --from runs_final
"""
import argparse
import json
from pathlib import Path

from src.common import paths
from src.common.paths import PROJECT_ROOT, RUNS_DIR, rel
from src.common.provenance import now_iso, write_json


def main(src: str) -> None:
    src_dir = PROJECT_ROOT / src / "selection"
    out = RUNS_DIR / "selection"
    out.mkdir(parents=True, exist_ok=True)
    for g in ("static", "dynamic", "hybrid"):
        v1 = json.loads((src_dir / f"{g}.json").read_text(encoding="utf-8"))
        write_json({"created": now_iso(), "group": g, "chosen": v1["chosen"], "fixed_from": rel(src_dir / f"{g}.json"),
                    "v1_chosen_run": v1.get("chosen_run"), "holdout_family": paths.HOLDOUT_FAMILY,
                    "note": "V2: architektúra pevne podľa výberu V1 (docs/09), výber sa neopakuje"}, out / f"{g}.json")
        (out / f"{g}.md").write_text(f"# Výber: {g}\n\nPevne podľa V1 (`{rel(src_dir)}`): **`{v1['chosen']}`** "
                                     f"(docs/09). Vynechaná rodina: {paths.HOLDOUT_FAMILY or '–'}.\n", encoding="utf-8")
        print(f"{g}: {v1['chosen']} (z V1)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", default="runs_final")
    main(ap.parse_args().src)
