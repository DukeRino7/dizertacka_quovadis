# Využívanie príznakov – static

> Generované `src/evaluation/feature_importance.py` (2026-11-02T00:00:18+01:00). Iba validácia, model seedu 0 posledného behu.
> Hodnota = pokles ROC-AUC po náhodnom premiešaní (priemer cez opakovania). Detail a grafy: `importance/` v behu modelu.

## Skupiny príznakov
| skupina | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| imports | 0.1534 | 0.0165 | 0.0068 | 0.1218 | 0.1242 |
| datadirectories | 0.0079 | 0.0021 | 0.0010 | 0.0068 | 0.0060 |
| section | 0.0016 | 0.0004 | 0.0002 | 0.0008 | 0.0008 |
| byteentropy | 0.0014 | 0.0010 | 0.0001 | 0.0006 | 0.0010 |
| histogram | 0.0008 | 0.0009 | 0.0003 | 0.0002 | 0.0004 |
| strings | 0.0008 | 0.0004 | 0.0002 | 0.0003 | 0.0006 |
| general | 0.0005 | 0.0001 | 0.0000 | 0.0002 | 0.0002 |
| exports | 0.0004 | 0.0000 | 0.0000 | 0.0001 | 0.0002 |
| header | 0.0003 | 0.0002 | 0.0003 | 0.0001 | 0.0001 |

## Sledované príznaky (možné artefakty datasetu)
| príznak | lr | rf | lightgbm | mlp_small | mlp_large |
|---|---|---|---|---|---|
| `general_has_signature` | 0.0001 | 0.0001 | 0.0000 | 0.0001 | 0.0000 |
| `datadir_CERTIFICATE_TABLE_size` | 0.0003 | 0.0001 | 0.0001 | 0.0001 | 0.0001 |
| `datadir_CERTIFICATE_TABLE_virtual_address` | 0.0002 | 0.0001 | -0.0000 | 0.0001 | 0.0001 |
| `header_coff_timestamp` | 0.0000 | 0.0000 | 0.0002 | 0.0000 | 0.0000 |
| `strings_urls` | 0.0000 | 0.0001 | 0.0000 | 0.0000 | 0.0000 |
| `datadir_RESOURCE_TABLE_size` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

Interpretácia: pokles blízko 0 = model sa bez príznaku zaobíde (často preto, že rovnakú informáciu nesú iné príznaky).
Permutácia jedného príznaku podhodnocuje skupinu korelovaných príznakov – preto aj kontrolný experiment bez nich
(`runs/comparison/static_ablations/`).
