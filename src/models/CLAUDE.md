# src/models/ – definície modelov

| Priečinok | Vstup | Úloha v experimente | Stav |
|---|---|---|---|
| `tabular/` | pevný vektor (EMBER / vektor z API / spojenie) | **spoločný rebríček** lr, rf, lightgbm, mlp_small, mlp_large pre static, dynamic aj hybrid | hotové |
| `static/` | EMBER príznaky | špecifické statické modely (zatiaľ žiadne – statické baseline sú v `tabular/`) | – |
| `dynamic/` | postupnosť API volaní | `seq_cnn` – sekvenčný model (vrstva B) | pripravené, čaká na dáta |
| `hybrid/` | oba vstupy | `two_branch` (kandidát na veľký model v kaskáde), neskorá fúzia | pripravené, čaká na dáta |
| `students_static/` | EMBER príznaky | ľahký statický model vytvorený destiláciou | neskôr |
| `students_dynamic/` | Speakeasy reporty | ľahký dynamický model vytvorený destiláciou | neskôr |

Úloha je binárna (malware/benign). Rodina malvéru sa používa iba na analýzu a stratifikáciu.
Dohodnutá sada modelov: `docs/03_protokol_a_modely.md`.
`registry.py` = register všetkých modelov (`model:` v konfigurácii → trieda); `torch_base.py` = spoločný
tréningový cyklus neurónových modelov vrstvy B (rovnaké pravidlá ako MLP v rebríčku).
