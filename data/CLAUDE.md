# data/ – pôvodné dáta (iba na čítanie)

**Obsah tohto priečinka sa nikdy nemení.** Žiadne úpravy, mazanie, premenovanie ani zápis výstupov.
Všetko odvodené patrí do `processed/`.

| Priečinok | Obsah | Zdroj |
|---|---|---|
| `quovadis-ember/` | statické EMBER priznaky (2381 float32 na vzorku) | https://huggingface.co/datasets/dtrizna/quovadis-ember |
| `quovadis-speakeasy/` | behaviorálne JSON reporty z emulácie Speakeasy | https://huggingface.co/datasets/dtrizna/quovadis-speakeasy |

- Speakeasy reporty pochádzajú z **emulácie**, nie z behu v plnohodnotnom Windows sandboxe.
- Párovanie výhradne podľa SHA-256. Zistenú štruktúru, počty a známe problémy popisuje `docs/01_audit_dat.md`.
- Podpriečinky `.cache/huggingface` patria nástroju na sťahovanie, nepoužívať ich ako dáta.
