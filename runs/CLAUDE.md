# runs/ – výsledky experimentov

Štruktúra: `runs/<prístup>/<model>/`, napr. statická logistická regresia → `runs/static/lr/`.
Každý prístup a model má vlastný priečinok, aby sa výsledky nemiešali.

| Priečinok | Obsah |
|---|---|
| `static/` | statické baseline modely |
| `dynamic/` | dynamické baseline modely |
| `hybrid/` | hybridné modely |
| `students_static/` | ľahké statické študentské modely |
| `students_dynamic/` | ľahké dynamické študentské modely |
| `cascade/` | finálna kaskáda a jej varianty |
| `static_ablations/` | kontrolné experimenty statických modelov (bez vybraných príznakov) |
| `comparison/` | spoločné porovnanie prístupov (tabuľky, grafy) |

Návrh obsahu priečinka modelu (zatiaľ neschválené):
```
runs/static/lr/
├── CLAUDE.md            súhrn modelu: čo to je, najlepší beh, hlavné výsledky
└── <dátum-čas>_<tag>/   jeden beh (opakovanie neprepíše predchádzajúci)
    ├── config.yaml      presná konfigurácia vrátane seedu
    ├── environment.json verzie knižníc, hardvér
    ├── model/           uložený model a naučené transformácie
    ├── predictions/     skóre a predikcie pre validáciu a test (sha256, label, score, pred)
    ├── metrics.json     detekčné metriky
    ├── timing.json      príprava priznakov, tréning, inferencia, pamäť
    ├── plots/           grafy (ROC, PR, matica zámen, ...)
    └── README.md        automaticky vygenerovaný súhrn behu
```
Predikcie podľa SHA-256 umožnia neskôr skladať kaskádu a porovnania bez opätovného spúšťania modelov.
