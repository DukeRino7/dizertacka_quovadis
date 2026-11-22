# data/ – pôvodné dáta (iba na čítanie)

**Obsah tohto priečinka sa nikdy nemení.** Žiadne úpravy, mazanie, premenovanie ani zápis výstupov.
Všetko odvodené patrí do `processed/`.

| Priečinok | Obsah | Zdroj |
|---|---|---|
| `quovadis-ember/` | statické EMBER priznaky (2381 float32 na vzorku) | https://huggingface.co/datasets/dtrizna/quovadis-ember |
| `quovadis-speakeasy/` | behaviorálne JSON reporty z emulácie Speakeasy | https://huggingface.co/datasets/dtrizna/quovadis-speakeasy |
| `kronodroid/` | Android (V4): 4 CSV so statickými a dynamickými príznakmi (emulátor aj skutočné zariadenie), `zip/` = pôvodné archívy, `csv/` = ich rozbalený obsah | https://github.com/aleguma/kronodroid (commit v `SOURCE_COMMIT.txt`, docs/18) |

- Speakeasy reporty pochádzajú z **emulácie**, nie z behu v plnohodnotnom Windows sandboxe.
- Párovanie výhradne podľa SHA-256. Zistenú štruktúru, počty a známe problémy popisuje `docs/01_audit_dat.md`.
- Podpriečinky `.cache/huggingface` patria nástroju na sťahovanie, nepoužívať ich ako dáta.
