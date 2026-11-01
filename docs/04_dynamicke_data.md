# 04 – Dynamické (Speakeasy) dáta

Stav k 2026-11-01: **kód pripravený, ostrý beh čaká na stiahnutie tréningovej časti** (stiahnutý je celý test,
z tréningu ~17 %). Kód bol overený iba na testovacích reportoch a iba ako kontrola správneho čítania formátu –
žiadne rozhodnutie o reprezentácii nevychádza z testu.

## Overený formát reportu (kontrola na testovacej časti)
- Súbor = JSON **zoznam vstupných bodov**; README datasetu opisuje iný tvar (`{"sha256", "entry_points"}`), ten v dátach nie je.
  SHA-256 je iba v názve súboru.
- Typy vstupných bodov: `module_entry`, `thread`, `tls_callback_N`; jedna vzorka môže mať aj vyše 100 vstupných bodov.
- API volanie: `pc`, `api_name`, `args` (vždy reťazce), `ret_val`. Názvy modulov majú rôznu veľkosť písmen
  (`kernel32` aj `KERNEL32`) → normalizácia na malé písmená.
- Voliteľné udalosti: `registry_access`, `file_access`, `network_events`, `process_events`, `dropped_files`, `handled_exceptions`.
- `error` = `{}` alebo popis ukončenia emulácie (`unsupported_api`, `max_api_count`, neplatný prístup do pamäte, ...).

## Popisné pozorovania na teste (nie podklad pre rozhodnutia)
- Emulácia `module_entry` končí chybou/limitom v 63–82 % vzoriek každej rodiny; najčastejšie `unsupported_api`
  (emulátor nepozná volanú funkciu) a `max_api_count` (limit 500 volaní).
- Limit 500 volaní dosiahne 42 % backdoorov, ale iba ~4 % benígnych súborov → **možný artefakt** (sledovať na tréningu).
- Malé reporty (≤ 5 volaní) sú v teste zriedkavé (0,4–6 % podľa rodiny); typicky jediné `VirtualAlloc(PAGE_EXECUTE_READWRITE)`
  – zbalená vzorka, emulácia skončila na začiatku. Na tréningu bolo zo zoznamu súborov podozrenie na 25 % malých
  ransomware reportov → **overiť auditom tréningu**.

## Postup spracovania (kód v `src/data/`)
| Krok | Modul | Výstup | Učí sa? |
|---|---|---|---|
| 1. audit | `audit_dynamic.py` | `processed/dynamic/audit/` (AUDIT.md, súhrn reportov, slovník API z tréningu, grafy) | nie |
| 2. normalizovaná cache | `build_dynamic.py` | `processed/dynamic/cache/<časť>.parquet` (+ `_args`) | nie |
| 3. pevný vektor pre rebríček | `build_dynamic_tabular.py` + `dynamic_features.py` | `processed/dynamic/tabular/` | slovník n-gramov iba z tréningu |

Reprezentácia pre spoločný rebríček (**NÁVRH**, `configs/data/dynamic.yaml`, potvrdiť po audite tréningu):
1- a 2-gramy postupnosti API volaní celej vzorky (top 2000 podľa dokumentovej frekvencie na tréningu, min. 5 vzoriek),
počty udalostí podľa typu, súhrnné príznaky reportu; surové počty (log a škálovanie robí model).
Argumenty volaní sa v rebríčku nepoužívajú; sú v cache pre sekvenčný model vrstvy B.

Hybrid (spoločný rebríček) = spojenie statického a dynamického vektora (ranná fúzia), `src/data/providers.py`.

## Otvorené rozhodnutia (po audite tréningu)
- čo s neúspešnými/malými reportmi (ponechať ako reálny výsledok emulácie, označiť príznakom, alebo vylúčiť –
  vylúčenie by zmenilo spoločné rozdelenie, preto by platilo pre všetky prístupy),
- veľkosť slovníka a rozsah n-gramov,
- či zahrnúť súhrnné príznaky, ktoré môžu niesť artefakty emulácie (počet volaní, chyby, dosiahnutý limit) –
  návrh: ponechať a overiť kontrolným experimentom ako pri statických dátach.

## Poradie spustenia po stiahnutí dát
```
.venv\Scripts\python.exe -m src.data.audit_dynamic            # 1. audit -> skontrolovať AUDIT.md a rozhodnúť
.venv\Scripts\python.exe -m src.data.build_dynamic            # 2. cache
.venv\Scripts\python.exe -m src.data.build_dynamic_tabular    # 3. vektor pre rebríček
.venv\Scripts\python.exe -m src.training.run_suite --approach dynamic
.venv\Scripts\python.exe -m src.training.run_suite --approach hybrid
```
