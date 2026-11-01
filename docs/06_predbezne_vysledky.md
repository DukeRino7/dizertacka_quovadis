# 06 – Predbežné výsledky (overenie postupu pred V1)

**Nie sú to finálne výsledky práce.** Slúžili na overenie, že postup funguje; finálne čísla budú z verzie `v1`.
Zdroj: `runs_predbezne/2026-11-01_pracovny_notebook_static/` (pracovný notebook, kód `28231d9`).

## Statická časť (test, prahy z validácie)
| Model | TPR @ FPR 1 % val → test | TPR @ FPR 0,1 % val → test | CPU čas/vz. (dávka) | Veľkosť |
|---|---|---|---|---|
| lr | 98,4 % → 96,7 % | 82,9 % → 7,3 % | 0,05 ms | 0,05 MB |
| rf | 99,5 % → 97,0 % | 98,5 % → 92,0 % | 0,09 ms | 32 MB |
| lightgbm | 99,8 % → 99,4 % | 99,0 % → 97,0 % | 0,68 ms | 38 MB |
| mlp_small | 99,3 % → 98,0 % | 95,5 % → 40,1 % | 0,33 ms | 0,35 MB |
| mlp_large | 99,5 % → 98,4 % | 96,4 % → 86,7 % | 0,51 ms | 12 MB |

Pozorovania:
- Najlepší a najstabilnejší pri časovom posune je LightGBM; pri FPR 0,1 % sa modely výrazne líšia (LR na teste zlyháva).
- Preučenie nie je (rozdiel ROC-AUC train − validácia 0,0002–0,001); všetky modely dokončili 30 pokusov ladenia.
- Kontrolný experiment bez podpisu a času zostavenia: LightGBM −0,4 b. (TPR @ FPR 1 %, test) → o artefakty sa takmer
  neopiera; LR −2,7 b., MLP pri FPR 0,1 % −7,5 b.
- Najdôležitejšia skupina príznakov pre všetky modely: importy.
- Pri LR a MLP tvorila väčšinu nákladov inferencie úprava vstupu (LR ~80 %) → v kóde pre V1 zrýchlená (float32, na mieste; 2× rýchlejšie).
- Nízka prevalencia (prepočet): pri 0,1 % malvéru aj LightGBM ~4,9 falošného poplachu na 1 skutočný (téza 2).
- Podskupiny: aj statické modely majú pri vzorkách s malým Speakeasy reportom 2–5× vyššie FPR (ťažké súbory, napr. zbalené).

## Reprodukovateľnosť
LR aj RF dali na súkromnom notebooku (Python 3.11) a pracovnom notebooku (Python 3.13) zhodné výsledky na 5 desatinných miest.

## Skúšobné behy dynamických a hybridných modelov (iba 5 000 vzoriek, 2 pokusy – iba kontrola funkčnosti)
Naznačujú výrazný pokles dynamických modelov z validácie na test (~0,98 → ~0,92 ROC-AUC) a vyššie skóre variantu
s udalosťami na validácii, ale nižšie na teste (konzistentné s artefaktom emulátora, docs/04). Hybrid ~0,99 na teste.
CPU čas/vzorku (orientačne): dynamický LightGBM 0,02 ms, dvojvetvová sieť 8,5 ms, sekvenčná CNN 59 ms.
