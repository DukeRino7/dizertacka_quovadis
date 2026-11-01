# src/models/ – definície modelov

Jeden priečinok na prístup, jeden súbor na model. Konkrétne architektúry zatiaľ **nie sú určené**.

| Priečinok | Vstup | Úloha v experimente |
|---|---|---|
| `static/` | EMBER priznaky | baseline samostatnej statickej detekcie; kandidáti na učiteľa |
| `dynamic/` | Speakeasy reporty | baseline samostatnej dynamickej detekcie; kandidáti na učiteľa |
| `hybrid/` | oba vstupy | baseline hybridnej detekcie; veľký model, ktorý v kaskáde rozhoduje pri nezhode |
| `students_static/` | EMBER priznaky | ľahký statický model vytvorený destiláciou |
| `students_dynamic/` | Speakeasy reporty | ľahký dynamický model vytvorený destiláciou |

Úloha je binárna (malware/benign). Rodina malvéru je dostupná, ale používa sa iba na analýzu a stratifikáciu,
pokiaľ sa nerozhodne inak.
