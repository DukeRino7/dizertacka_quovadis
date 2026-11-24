# Využívanie príznakov – dynamic

> Generované `src/evaluation/feature_importance.py` (2026-11-23T20:26:12+01:00). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
| skupina | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| syscalls | 0.3670 | 0.4742 | 0.4836 | 0.4688 | 0.4736 |
| total | 0.0134 | 0.0008 | 0.0012 | 0.0065 | 0.0066 |

## Sledované príznaky (možné artefakty datasetu)
| príznak | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| `general_has_signature` | – | – | – | – | – |
| `datadir_CERTIFICATE_TABLE_size` | – | – | – | – | – |
| `datadir_CERTIFICATE_TABLE_virtual_address` | – | – | – | – | – |
| `header_coff_timestamp` | – | – | – | – | – |
| `strings_urls` | – | – | – | – | – |
| `datadir_RESOURCE_TABLE_size` | – | – | – | – | – |

Interpretácia: pokles blízko 0 = model sa bez príznaku zaobíde (často preto, že rovnakú informáciu nesú iné príznaky).
Permutácia jedného príznaku podhodnocuje skupinu korelovaných príznakov – preto aj kontrolný experiment bez nich
(`runs/comparison/static_ablations/`).
