# Spustenie experimentu (napr. na pracovnom notebooku)

Claude ani prihlásenie do Claude **netreba** – všetko robia skripty v PowerShelli. Potrebný je Python 3.11 – 3.13,
internet a pre neurónové siete grafická karta NVIDIA s aktuálnym ovládačom.

## 1. Získať projekt
- **Odporúčané:** `git clone https://github.com/DukeRino7/dizertacka_quovadis.git` (prihlásenie na GitHub) – finálny beh
  si potom zapíše presnú verziu kódu (commit) do `RUN_INFO.txt`;
- alebo **ZIP konkrétnej verzie**: GitHub → *Tags* → napr. `v1` → *Source code (zip)* – bez prihlasovania v gite
  (vhodné na pracovnom počítači s iným GitHub účtom); verzia sa zapíše z `VERSION.txt` do výsledkov každého behu.

## 0. Dohodnutý postup V1 (2026-11-01)
Všetko počíta **pracovný notebook** (tréning, destilácia, kaskády aj merania spotreby → jeden počítač);
**PC** slúži na kontrolu výsledkov, commit do gitu (záloha) a rozhodnutia. Po večeroch: večer spustiť skript,
ráno prípadne zastaviť **Ctrl+C**, večer spustiť znova (hotové kroky/modely sa preskočia, stratí sa iba rozpracovaný model).

| # | Kde | Čo |
|---|---|---|
| 0 | notebook | predbežný test statickej časti |
| 1 | PC | kontrola testu, opravy → značka `v1` |
| 2 | notebook | ZIP `v1` → `setup.ps1` → `run_static.ps1` |
| 3 | notebook | Speakeasy skopírovať z PC do `data\quovadis-speakeasy` (aj s `.cache`) → `run_dynamic.ps1` (1–2 večery) |
| 4 | notebook | `run_hybrid.ps1` (1–2 večery) |
| 5 | notebook | `run_distillation_cascade.ps1` |
| 6 | PC | kontrola, záverečný report, commit → V1 hotová; potom V2 (zero-day) |

Po každom kroku preniesť priečinok `runs\` (ZIP) na PC. **Kde sme:** `powershell -ExecutionPolicy Bypass -File scripts\status.ps1`.
Pri meraniach spotreby: notebook v sieti (nie na batérii), režim vysokého výkonu, ostatné programy zavreté.

## 2. Príprava (raz)
```
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```
`.venv` + knižnice, kontrola GPU, EMBER (zafixovaná revízia), statické dáta + overenie „ZHODA“ s gitom.

## 3. Postup po častiach (predbežná fáza)
| Skript | Čo robí | Trvanie (odhad, notebook) |
|---|---|---|
| `scripts\run_static.ps1` | statické modely, spotreba, analýza príznakov, kontrolné experimenty, porovnanie | 4–7 h |
| `scripts\run_dynamic.ps1` | Speakeasy (overenie), audit, dynamické dáta, dynamické modely, kontrolné experimenty | ~0,5 dňa |
| `scripts\run_hybrid.ps1` | hybridné modely, spotreba, porovnanie | ~0,5 dňa |
| `scripts\run_distillation_cascade.ps1` | výber modelov podľa pravidla, učitelia, študenti, kaskády, záverečný report | ~0,5 dňa |

Každý skript po prerušení stačí spustiť znova – hotové kroky sa preskočia (značky v `runs\_state\`).
Krok zopakuješ zmazaním jeho značky. Výpisy: `runs\*_log.txt`.

## 4. Finálny beh (všetko naraz, 2–3 dni)
Po predbežnej fáze, keď sú rozhodnutia zapísané v `configs\` a kód je zmrazený (značka v gite, napr. `final-v1`):
```
powershell -ExecutionPolicy Bypass -File scripts\run_all.ps1 -RunsDir runs_final
```
Všetko sa uloží do `runs_final\` (oddelene od predbežných výsledkov), vrátane `RUN_INFO.txt` (počítač, commit, čas).
Pri finálnom behu by mal byť Speakeasy dataset už stiahnutý alebo skopírovaný do `data\quovadis-speakeasy`.

## 5. Prenos výsledkov
Zabaliť priečinok s výsledkami (`runs\` alebo `runs_final\`) a preniesť na PC, alebo `git push`.
Uložené modely (`model\` v behoch) nie sú v gite, ale sú v týchto priečinkoch.
**Merania spotreby porovnávať iba z jedného počítača** (`environment.json` v každom behu = názov počítača a hardvér).

## 6. Verzia V2 (zero-day + kaskáda B, docs/09)
Spúšťa sa **v priečinku projektu z V1** na pracovnom notebooku (tam sú `data\`, `processed\`, `.venv\`, `runs_final\`):
1. GitHub → *Tags* → `v2` → *Source code (zip)* a obsah ZIP-u **rozbaliť cez existujúci priečinok V1**
   (prepíše sa iba kód, dokumenty a konfigurácie; dáta, `processed\` a výsledky V1 ostanú).
2. Kontrola (~1 h, odporúčané):
   `powershell -ExecutionPolicy Bypass -File scripts\run_v2.ps1 -Smoke -Families rat` → výsledky v `runs_v2_smoke\`
   (iba technická kontrola, nie výsledky; potom priečinok `runs_v2_smoke\` možno zmazať).
3. Celý beh (2–3 večery, pokračuje po prerušení – stačí spustiť znova):
   `powershell -ExecutionPolicy Bypass -File scripts\run_v2.ps1`
4. Na súkromný notebook preniesť `runs_v2\` **bez uložených modelov** (modely majú ~7 GB a na vyhodnotenie netreba):
   `robocopy runs_v2 E:\runs_v2 /E /XD model` (E: = USB). Súhrn: `runs_v2\comparison\v2\README.md`.

**Alternatíva – samostatný priečinok:** ZIP `v2` rozbaliť do nového priečinka (napr. `dizertacka_quovadis-2`) a skopírovať
doň z priečinka V1 `data\`, `processed\` a `.venv\` (`runs_final\` bez modelov je už v ZIP-e a na V2 stačí).
Ak by skopírované `.venv\` nefungovalo, spustiť v novom priečinku `scripts\setup.ps1`. Pozor na voľné miesto na disku.

Čo beh V2 robí: (1) `runs_v2\full` – učiteľ dvojvetvová sieť, noví študenti (ladenie 30 pokusov) a ich meranie spotreby,
kaskády B na modeloch V1; (2) `runs_v2\lofo\<rodina>` – pre každú zo 7 rodín slovníky API bez rodiny, celý rebríček
modelov s hyperparametrami z V1, učitelia, študenti, kaskády A aj B; (3) súhrn a vyhodnotenie téz.
Dočasné dáta zero-day behov: `processed\dynamic\lofo\` (~7,5 GB, dajú sa po behu zmazať).

## 7. Verzia V3 (špecialista pre neisté súbory + prekalibrovanie prahu, docs/12)
Spúšťa sa **v priečinku, kde bežala V2** (na pracovnom notebooku `dizertacka_quovadis-2`). Potrebné sú `data\`, `processed\`
(aj `processed\dynamic\lofo\` z V2 – ak chýba, skript ho znova vytvorí), `.venv\`, `runs_final\` a `runs_v2\`.
Modely netreba, stačia uložené predikcie a `teachers\`.
1. GitHub → *Tags* → `v3` → *Source code (zip)* a ZIP rozbaliť do **dočasného** priečinka (napr. `Downloads\v3`).
2. Do priečinka V2 skopírovať **iba kód a dokumenty** (dáta a výsledky V1/V2 ostanú nedotknuté). V PowerShelli:
   ```
   $Z = "$HOME\Downloads\v3\dizertacka_quovadis-3"
   $P = "D:\dizertacka\dizertacka_quovadis-2"
   robocopy $Z $P /E /XD "$Z\data" "$Z\processed" "$Z\runs" "$Z\runs_final" "$Z\runs_v2"
   ```
   `$Z` = rozbalený priečinok, v ktorom je `SETUP.md`; `$P` = priečinok, kde bežala V2 (obe cesty upraviť podľa
   skutočnosti). Vylúčenie je cez celé cesty, aby sa neprepísali dáta ani výsledky, ale skopíroval sa kód vrátane `src\data`.
   Potom `cd $P` a pokračovať ďalším krokom.
3. Kontrola (~5 min): `powershell -ExecutionPolicy Bypass -File scripts\run_v3.ps1 -Smoke -Families rat`
   → `runs_v3_smoke\` (iba technická kontrola; potom ho možno zmazať).
4. Celý beh (odhad 30–60 min, pokračuje po prerušení): `powershell -ExecutionPolicy Bypass -File scripts\run_v3.ps1`
5. Preniesť bez modelov: `robocopy runs_v3 E:\runs_v3 /E /XD model`. Súhrny: `runs_v3\comparison\v3\README.md` (B)
   a `RECALIBRATION.md` (C).

Čo beh V3 robí: (1) `runs_v3\full` – špecialisti (4 varianty × 3 seedy) na rozdelení V1 a meranie ich CPU času;
(2) `runs_v3\lofo\<rodina>` – to isté pre 7 vynechaných rodín, komponenty z `runs_v2\lofo\<rodina>`;
(3) súhrn kritérií B1–B3 a scenár C (prekalibrovanie prahu, iba z uložených predikcií).
Merania CPU času porovnávať iba s V1/V2 z toho istého počítača.
