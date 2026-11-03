# src/cascade/ – finálna kaskáda

1. Statický a dynamický model (finálne: študenti z destilácie) ohodnotia vzorku pri svojich prahoch z validácie.
2. Ak sa zhodnú na malware alebo benign, rozhodnutie je konečné.
3. Ak sa nezhodnú, rozhodne veľký hybridný model.

| Modul | Úloha |
|---|---|
| `components.py` | načítanie uložených predikcií, prahov a benchmarkov komponentov (`'<prístup>/<model>'` alebo cesta k behu) |
| `evaluate_b.py` | **kaskáda B** (V2, docs/09): statický model → pri neistom skóre emulácia + dynamický → pri nezhode hybrid (`second_stage: dynamic`) alebo rovno hybrid (`hybrid`); pásmo neistoty z validácie, krivka rozpočtov emulácie, podiel emulovaných súborov, TPR na januárových vzorkách vynechanej rodiny → `runs*/cascade/b_*/` |
| `evaluate.py` | vyhodnotenie z uložených predikcií: kvalita kaskády vs. hybrid na každej vzorke, samostatní študenti, neskorá fúzia (priemer, stacking); podiel eskalácií, chyby pri zhode, prínos hybridu na eskalovaných vzorkách; odhad nárokov z benchmarkov → `runs/cascade/<variant>/<beh>/` |

Rozhodnuté: prahy študentov aj hybridu = prah pre FPR ≤ 1 % na validácii (`configs/protocol.yaml`).
Neskorá fúzia je v `src/models/hybrid/late_fusion.py`.
`components.py`: premenná `DIZERTACKA_RESULTS_FALLBACK` (napr. `runs_final`) – komponent sa hľadá aj tam (kaskády B na modeloch V1); v zero-day behoch sa nepoužíva.
Plánované: meranie nárokov celej kaskády skutočným spustením modelov (nielen odhad zo súčtu komponentov).
Podrobnosti: `docs/05_destilacia_a_kaskada.md`.
