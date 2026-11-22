# configs/ – konfigurácie experimentov

**`protocol.yaml` = spoločné pravidlá tréningu a vyhodnotenia pre všetky modely** (ladenie, seedy, váhy tried, prahy, meranie času).

Jedna konfigurácia = jeden experiment. Štruktúra kopíruje `runs/` a `src/models/`:

| Priečinok | Čo konfiguruje | Výsledky idú do |
|---|---|---|
| `data/` | index, rozdelenie a predspracovanie dát | `processed/` |
| `static/` | statické baseline modely (EMBER) | `runs/static/<model>/` |
| `dynamic/` | dynamické baseline modely (Speakeasy) | `runs/dynamic/<model>/` |
| `hybrid/` | hybridné modely (oba vstupy) | `runs/hybrid/<model>/` |
| `students_static/` | ľahké statické modely z destilácie | `runs/students_static/<model>/` |
| `students_dynamic/` | ľahké dynamické modely z destilácie | `runs/students_dynamic/<model>/` |
| `cascade/` | finálna kaskáda (výber študentov, učiteľa, prahov) | `runs/cascade/<variant>/` |
| `kronodroid/` | V4: dataset KronoDroid (zdroj, skupiny stĺpcov, príprava dát, vynechávané rodiny) | `processed/kronodroid/` |
| `kronodroid/cascade/` | V4: 12 kaskád A/B a 4 špecialisti (obdoby `cascade/`; komplexný hybrid = `hybrid/mlp_large`) | `runs_v4/<vetva>/*/cascade/` |
| `kronodroid/dynamic_ablations/` | V4: D-norm – dynamické aj hybridné modely na podieloch volaní, hyperparametre z pôvodných | `runs_v4/<vetva>/full/dynamic_ablations/` |

Návrh konvencií (zatiaľ neschválené):
- Formát YAML, názov súboru = názov modelu, napr. `configs/static/lr.yaml`.
- Konfigurácia obsahuje všetko potrebné na zopakovanie behu: seed, hyperparametre, vstupné dáta, rozdelenie.
- Pri behu sa konfigurácia skopíruje do priečinka behu, aby výsledok vždy niesol presné nastavenie.
