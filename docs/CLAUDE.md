# docs/ – súhrnné dokumenty pre dizertáciu

Texty, z ktorých sa budú preberať informácie do práce. Číslované podľa poradia etáp.

| Súbor | Obsah | Stav |
|---|---|---|
| `00_vyskumne_otazky.md` | výskumné otázky a pravidlá výberu modelov (učiteľ, študent) | dohodnuté |
| `01_audit_dat.md` | štruktúra datasetov, párovanie, označenia, zistené problémy | EMBER overený, Speakeasy čiastočne |
| `02_staticke_data.md` | spoločné rozdelenie a predspracovanie statických dát | hotové |
| `03_protokol_a_modely.md` | dohodnutá sada modelov a spoločný trénovací protokol | protokol = NÁVRH |
| `05_destilacia_a_kaskada.md` | dohodnutý postup destilácie a vyhodnotenia kaskády | dohodnuté, implementácia po baseline |
| `06_predbezne_vysledky.md` | predbežné výsledky (overenie postupu pred V1), nie finálne | hotové |
| `04_dynamicke_data.md` | formát Speakeasy reportov, postup spracovania, otvorené rozhodnutia | hotové (rozhodnutie: iba API volania) |
| `07_vysledky_v1.md` | **finálne výsledky V1** (`runs_final/`): odpovede na otázky a tézy, kaskáda, komplementarita, nároky, návrhy pre V2 | hotové 2026-11-03 |
| `08_zhrnutie_v1.md` | stručné zhrnutie V1 pre vedúcu: dáta, modely, súhrnná tabuľka, najlepší podľa parametrov, tézy, otázky na konzultáciu | hotové 2026-11-03 |
| `09_plan_v2.md` | **plán V2** (zero-day = vynechanie rodiny, kaskáda B, spresnenie téz, kritériá vopred) | dohodnuté 2026-11-03 |
| `10_vysledky_v2.md` | **výsledky V2** (`runs_v2/`): časový test, zero-day po rodinách, krivka rozpočtu emulácie, tézy podľa kritérií docs/09 | hotové 2026-11-04 |
| `11_zhrnutie_v2.md` | stručné zhrnutie V2 pre vedúcu: súhrnná tabuľka, zistenia, tézy, otázky na konzultáciu | hotové 2026-11-04 |
| `12_plan_v3.md` | **plán V3** (zdôvodnenie z analýzy príčin V2; B: druhý stupeň učený na neistých súboroch, C: prekalibrovanie prahu na nových neškodných súboroch; kritériá vopred) | rozhodnuté 2026-11-04 (autor), pred výsledkami |
| `13_vysledky_v3.md` | **výsledky V3** (`runs_v3/`): špecialista (kritériá B1–B3, porovnanie pri rovnakom FPR), prekalibrovanie prahu, výpočtové nároky (emulácia nemerateľná, 60 s = horná hranica), stav téz po V1–V3 | hotové 2026-11-07 |
| `14_zhrnutie_v1_v3.md` | zhrnutie V1–V3 pre vedúcu: čo sa robilo, stav téz, hlavné zistenia, obmedzenia, otázky na konzultáciu | hotové 2026-11-07 |
| `15_zhrnutie_pre_veducu.pdf` | 4-stranové PDF pre vedúcu písané pre laika (slovník pojmov, obrázok kaskády, bez skratiek): techniky, výsledky, stav téz, zistenia, overenie robustnosti, návrhy alternatívnych téz s výsledkami (čísla z docs/07, 10, 13, 17) | hotové 2026-11-07 |
| `16_plan_robustnost.md` | plán overenia robustnosti: štatistická významnosť (bootstrap), citlivosť na chybu emulácie; kritériá vopred | rozhodnuté 2026-11-07, pred výpočtom |
| `17_vysledky_robustnost.md` | výsledky overenia robustnosti: hlavné tvrdenia významné, prekalibrovanie spoľahlivé pri ~1 600 súboroch, zistenie D platí aj pri úspešnej emulácii (dynamika tam škodí) | hotové 2026-11-07 |

Pravidlá:
- Uvádzať iba overené fakty s popisom, ako boli overené. Návrhy a otvorené rozhodnutia jasne označiť.
- Čísla preberať z výstupov skriptov alebo z `runs/`, nikdy ich neodhadovať.
