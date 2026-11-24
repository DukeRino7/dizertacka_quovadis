# Využívanie príznakov – hybrid

> Generované `src/evaluation/feature_importance.py` (2026-11-23T00:18:37+01:00). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
| skupina | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| static:permissions | 0.2137 | 0.2014 | 0.1894 | 0.2570 | 0.2607 |
| dynamic:syscalls | 0.1277 | 0.1616 | 0.1140 | 0.1106 | 0.1309 |
| static:metadata | 0.0074 | 0.0088 | 0.0100 | 0.0082 | 0.0109 |
| dynamic:total | 0.0001 | 0.0001 | -0.0001 | 0.0005 | 0.0002 |

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
