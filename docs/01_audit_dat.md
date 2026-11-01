# 01 – Audit dát

Stav k 2026-11-01. EMBER overený na stiahnutých súboroch. Speakeasy overený zo zoznamu súborov repozitára
na Hugging Face (`data/quovadis-speakeasy/.cache/huggingface/trees/*.json`, obsahuje cesty a veľkosti všetkých
súborov), obsah reportu zatiaľ iba na jednej testovacej vzorke. **Po dokončení sťahovania treba audit
zopakovať reprodukovateľným skriptom v `src/data/` na skutočných súboroch.**

## Zdroje
- Statické: https://huggingface.co/datasets/dtrizna/quovadis-ember
- Behaviorálne: https://huggingface.co/datasets/dtrizna/quovadis-speakeasy (emulácia Speakeasy, nie Windows sandbox)
- Pôvodné práce: Trizna et al., *Quo Vadis* (AISec 2022), *Nebula* (IEEE TIFS 2024)

## Pôvodné rozdelenie
Časové: tréning zozbieraný v januári 2022, test v apríli 2022 (podľa README oboch datasetov).

## EMBER – štruktúra
`{train,test}/<trieda>/` s triedami benign, backdoor, coinminer, dropper, keylogger, ransomware, rat, trojan.
Každý priečinok obsahuje:
- `features.npy` – float32, 2381 stĺpcov (EMBER priznaky, Anderson & Roth 2018),
- `hashes.txt` – riadky `index,sha256` úspešne spracovaných súborov,
- `errors.log` – riadky `index,sha256,chyba` zlyhaných súborov.

**Dôležité:** riadky zlyhaných súborov v `features.npy` zostali (sú nulové). Počet riadkov matice = úspešné + zlyhané.
Riadok vzorky určuje index z `hashes.txt`. Overené: každý takto určený riadok je nenulový, počet nulových riadkov
sa rovná počtu chýb, žiadne NaN.

| Časť | Trieda | Použiteľné | Chyby extrakcie |
|---|---|---:|---:|
| train | benign | 24 416 | 18 |
| train | backdoor | 11 061 | 1 |
| train | coinminer | 6 548 | 343 |
| train | dropper | 8 243 | 0 |
| train | keylogger | 4 378 | 0 |
| train | ransomware | 9 627 | 0 |
| train | rat | 1 697 | 0 |
| train | trojan | 8 733 | 0 |
| test | benign | 7 940 | 4 |
| test | backdoor | 1 940 | 0 |
| test | coinminer | 1 684 | 0 |
| test | dropper | 252 | 0 |
| test | keylogger | 1 041 | 0 |
| test | ransomware | 2 139 | 0 |
| test | rat | 1 258 | 0 |
| test | trojan | 1 085 | 0 |

Spolu: train 74 703 (benign 24 416, malware 50 287), test 17 339 (benign 7 940, malware 9 399).
Chyby: 21× chyba knižnice LIEF (`lief.PE.Section` bez `CHARACTERISTICS`), 345× súbor PE sa nenašiel
(z toho 1 záznam nie je vzorka, ale `sha_path_db.csv.err`).
README uvádza 93 533 súborov; použiteľných je menej kvôli týmto chybám.

## Speakeasy – štruktúra (zo zoznamu súborov)
- `windows_emulation_{trainset,testset}/report_<trieda>/`, benígne sú `report_clean` a `report_windows_syswow64`.
- Názvy: train `<sha256>.json`, test `<sha256>.dat.json`.
- Train `report_backdoor` a `report_clean` majú ďalšiu úroveň podpriečinkov (napr. `report_clean/0/<sha256>.json`).
- `report_windows_syswow64` (train 235 + 1 `.err`, test 59) je pomenovaný podľa programu (napr. `WerFault.json`),
  nie podľa SHA-256 → **nedá sa spárovať**, v EMBER chýba.
- Niekoľko `.err` súborov s veľkosťou 0 B (nie sú reporty).
- Celková veľkosť ~5,5 GB.
- Formát reportu (overené na 1 testovacej vzorke a `example-ransomware.json`): JSON **zoznam** vstupných bodov
  (`ep_type`, `start_addr`, `ep_args`, `apihash`, `apis`, `ret_val`, `error`, `dynamic_code_segments`);
  každé API volanie má `pc`, `api_name`, `args`, `ret_val`. README opisuje iný tvar (`{"sha256", "entry_points"}`),
  ten sa v dátach nenachádza. SHA-256 je iba v názve súboru.
- `speakeasy-config.json`: `timeout` 60, `max_api_count` 500 (pri testovacej vzorke bolo v module_entry 501 volaní).

## Párovanie podľa SHA-256
- Všetkých **91 596** unikátnych SHA-256 z EMBER má Speakeasy report. Žiadna EMBER vzorka nie je bez páru.
- Všetky páry majú zhodnú triedu a zhodnú časť (train/test), okrem nižšie uvedených duplicít.
- Iba v Speakeasy (365): presne tie súbory, pri ktorých zlyhala EMBER extrakcia (343 coinminer, 18 + 4 clean).

## Zistené problémy
1. **Prekryv train/test:** 446 SHA-256 je v train aj test (všetky keylogger; 43 % testovacích keyloggerov).
   *Riešenie zatiaľ neschválené* (návrh: vyradiť z tréningu, test ponechať pôvodný).
2. **Identické EMBER vektory pri rôznych SHA-256:** 131 skupín, 268 vzoriek, max. 3 v skupine. Žiadna skupina
   neprechádza cez train/test a žiadna nemá rozporné označenie. *Návrh:* pri vyčleňovaní validácie držať skupinu spolu.
3. **Malé Speakeasy reporty (< 1 kB):** train ransomware 2 391 z 9 627 (25 %), rat 166, dropper 72, clean 204;
   v teste spolu 88. Možné neúspešné emulácie, riziko skratky pre dynamický model. *Treba overiť obsah.*
4. **Zmena zloženia tried medzi train a test** (napr. dropper 8 243 vs 252, rat 1 697 vs 1 258) – súčasť časového
   posunu; ovplyvní interpretáciu výsledkov podľa rodín.

## Otvorené rozhodnutia
- spôsob riešenia prekryvu (bod 1),
- veľkosť a spôsob vyčlenenia validácie (návrh: 10–15 % tréningu, stratifikovane podľa rodiny),
- zaobchádzanie s malými/prázdnymi reportmi (až po kontrole obsahu).
