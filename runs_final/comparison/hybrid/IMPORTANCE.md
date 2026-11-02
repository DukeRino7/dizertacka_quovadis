# Využívanie príznakov – hybrid

> Generované `src/evaluation/feature_importance.py` (2026-11-02T20:49:25+01:00). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
| skupina | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| static:imports | 0.0278 | 0.0065 | 0.0024 | 0.0703 | 0.0265 |
| dynamic:api_2gram | 0.0179 | 0.0010 | 0.0001 | 0.0321 | 0.0093 |
| static:datadirectories | 0.0019 | 0.0036 | 0.0018 | 0.0138 | 0.0016 |
| static:section | 0.0006 | 0.0003 | 0.0002 | 0.0009 | 0.0004 |
| dynamic:api_1gram | 0.0005 | 0.0002 | 0.0000 | 0.0009 | 0.0004 |
| static:byteentropy | 0.0003 | 0.0006 | 0.0002 | 0.0005 | 0.0006 |
| static:strings | 0.0003 | 0.0004 | 0.0002 | 0.0006 | 0.0004 |
| static:histogram | 0.0002 | 0.0004 | 0.0003 | 0.0001 | 0.0003 |
| static:general | 0.0002 | 0.0004 | 0.0001 | 0.0004 | 0.0002 |
| static:exports | 0.0001 | 0.0000 | 0.0000 | 0.0001 | 0.0001 |
| static:header | 0.0001 | 0.0003 | 0.0003 | 0.0001 | 0.0000 |

## Sledované príznaky (možné artefakty datasetu)
| príznak | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| `general_has_signature` | 0.0001 | 0.0003 | 0.0000 | 0.0003 | 0.0001 |
| `datadir_CERTIFICATE_TABLE_size` | 0.0001 | 0.0004 | 0.0001 | 0.0003 | 0.0001 |
| `datadir_CERTIFICATE_TABLE_virtual_address` | 0.0001 | 0.0002 | 0.0000 | 0.0002 | 0.0001 |
| `header_coff_timestamp` | 0.0000 | 0.0001 | 0.0002 | 0.0000 | 0.0000 |
| `strings_urls` | 0.0000 | 0.0002 | 0.0000 | 0.0000 | 0.0000 |
| `datadir_RESOURCE_TABLE_size` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

Interpretácia: pokles blízko 0 = model sa bez príznaku zaobíde (často preto, že rovnakú informáciu nesú iné príznaky).
Permutácia jedného príznaku podhodnocuje skupinu korelovaných príznakov – preto aj kontrolný experiment bez nich
(`runs/comparison/static_ablations/`).
