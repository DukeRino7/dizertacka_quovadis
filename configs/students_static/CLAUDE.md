# configs/students_static/

Ľahký static študent pre kaskádu (docs/05_destilacia_a_kaskada.md). Výsledky v `runs/students_static/<názov>/`.

| Súbor | Obsah |
|---|---|
| `mlp_kd.yaml` | malé MLP učené destiláciou (strata α·skutočné + (1−α)·T²·učiteľ; α, T sa ladia na validácii) |
| `mlp_nokd.yaml` | **kontrola**: rovnaké MLP a rovnaký priestor bez destilácie |

Postup: 1) vybrať učiteľa podľa `docs/00_vyskumne_otazky.md` a doplniť `distillation.teacher`;
2) `python -m src.training.teacher_oof --teacher <prístup>/<model>` (mäkké označenia krížovo);
3) `python -m src.training.run_tabular --config configs/students_static/mlp_kd.yaml` a `mlp_nokd.yaml`.
Veľkosť študenta (1 vrstva, 16–64 neurónov) je NÁVRH – overiť benchmarkom pravidlo „aspoň 10× lacnejší než učiteľ“.
