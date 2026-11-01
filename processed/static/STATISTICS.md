# Štatistiky statického datasetu (EMBER)

> Automaticky generované skriptom `src/data/build_static.py` (2026-11-01T16:26:34+01:00).
> Všetky čísla pochádzajú priamo z dát v `processed/static`. Štatistiky príznakov (časť 3) sú počítané
> **iba na tréningu**. Porovnania s validáciou a testom (časti 4–5) sú iba popisné a nevyužívajú sa
> na žiadne rozhodnutie o spracovaní ani modeloch.

## 1. Rozmery a integrita
| časť | vzorky | príznaky | NaN | ±Inf | veľkosť X [MB] |
|---|---|---|---|---|---|
| train | 66 831 | 2381 | 0 | 0 | 636 |
| validácia | 7 426 | 2381 | 0 | 0 | 71 |
| test | 17 339 | 2381 | 0 | 0 | 165 |

- Typ: float32; riadky zoradené podľa `processed/index/samples.parquet` (časť → rodina → SHA-256).
- Overené: poradie SHA-256 v `meta_*.parquet` sa zhoduje s indexom; každý riadok X je zhodný s pôvodným
  `features.npy` (kontrola na 600 náhodných riadkoch, max. odchýlka 0.0).

## 2. Vzorky podľa rodiny a časti
| rodina | train | validation | test |
|---|---|---|---|
| benign | 21 974 | 2 442 | 7 940 |
| backdoor | 9 955 | 1 106 | 1 940 |
| coinminer | 5 893 | 655 | 1 684 |
| dropper | 7 419 | 824 | 252 |
| keylogger | 3 539 | 393 | 1 041 |
| ransomware | 8 665 | 962 | 2 139 |
| rat | 1 527 | 170 | 1 258 |
| trojan | 7 859 | 874 | 1 085 |
| SPOLU | 66 831 | 7 426 | 17 339 |

Podiel malvéru: train 0.671, validácia 0.671, test 0.542

Graf: `plots/class_distribution.png`

## 3. Príznaky podľa skupín (iba tréning)
| skupina | šírka | typ | konštantné (train) | takmer konšt. (≥0.999) | medián podielu nenul. | min | max | medián max/q99 |
|---|---|---|---|---|---|---|---|---|
| histogram | 256 | distribution | 0 | 0 | 0.9994 | 0 | 0.9992 | 22.59 |
| byteentropy | 256 | distribution | 0 | 0 | 0.879 | 0 | 0.9981 | 13.08 |
| strings | 104 | mixed | 0 | 0 | 0.9983 | 0 | 1.056e+08 | 11.13 |
| general | 10 | mixed | 0 | 0 | 0.4189 | 0 | 1.399e+09 | 1 |
| header | 62 | mixed | 32 | 37 | 0.0001721 | -2 | 4.295e+09 | 2.043 |
| section | 255 | mixed | 28 | 56 | 0.009532 | -1.399e+09 | 5.369e+08 | 9 |
| imports | 1 280 | hashed | 0 | 73 | 0.07011 | -768 | 1465 | 5 |
| exports | 128 | hashed | 0 | 0 | 0.007938 | -545 | 535 | 23.5 |
| datadirectories | 30 | count | 2 | 6 | 0.1951 | 0 | 1.399e+09 | 29.47 |

- *konštantné* = jediná hodnota na celom tréningu (pre model bez informácie); spolu
  **62** z 2381.
- *takmer konšt.* = najčastejšia hodnota pokrýva aspoň 0.999 tréningových vzoriek; spolu
  **172**.
- *medián max/q99* = typický pomer maxima a 99. percentilu v stĺpci; vysoké hodnoty znamenajú ťažké chvosty
  (dôvod pre log-transformáciu pri lineárnych modeloch a neurónových sieťach).
- Záporné hodnoty sa vyskytujú v skupinách: `header`, `section`, `imports`, `exports` (hašované bloky používajú znamienkový FeatureHasher).

Graf: `plots/feature_sparsity_by_group.png`; úplná tabuľka: `train_feature_stats.parquet`.

## 4. Posun rozdelenia príznakov (popisné)
Dvojvýberová KS štatistika D po príznakoch, náhodná podvzorka max. 20000 vzoriek z každej časti
(seed 42). Validácia je náhodne vyčlenená z rovnakého obdobia ako tréning, preto slúži ako referencia
„bez posunu“; test je zozbieraný o 3 mesiace neskôr.

| skupina | val: medián | val: max | test: medián | test: max |
|---|---|---|---|---|
| histogram | 0.01126 | 0.0196 | 0.07639 | 0.1526 |
| byteentropy | 0.01085 | 0.02167 | 0.07486 | 0.1514 |
| strings | 0.009965 | 0.02151 | 0.07836 | 0.1548 |
| general | 0.005695 | 0.01588 | 0.113 | 0.1906 |
| header | 0 | 0.01337 | 0 | 0.2393 |
| section | 0.0008724 | 0.01723 | 0.002747 | 0.2258 |
| imports | 0.002614 | 0.01662 | 0.02153 | 0.1834 |
| exports | 0.000904 | 0.003249 | 0.001037 | 0.02249 |
| datadirectories | 0.004877 | 0.01884 | 0.1012 | 0.2292 |

Najväčší posun train → test (25 príznakov):

| stĺpec | príznak | skupina | KS train–test | KS train–val |
|---|---|---|---|---|
| 626 | header_coff_timestamp | header | 0.2393 | 0.007201 |
| 2 355 | datadir_RESOURCE_TABLE_size | datadirectories | 0.2292 | 0.01406 |
| 736 | section_size_hash_43 | section | 0.2258 | 0.01246 |
| 836 | section_vsize_hash_43 | section | 0.2132 | 0.01392 |
| 825 | section_vsize_hash_32 | section | 0.1939 | 0.01557 |
| 2 375 | datadir_IAT_size | datadirectories | 0.1929 | 0.0114 |
| 617 | general_vsize | general | 0.1906 | 0.01588 |
| 2 356 | datadir_RESOURCE_TABLE_virtual_address | datadirectories | 0.1888 | 0.01505 |
| 1 659 | imports_function_hash_0460 | imports | 0.1834 | 0.008301 |
| 620 | general_imports | general | 0.1806 | 0.01339 |
| 1 252 | imports_function_hash_0053 | imports | 0.1781 | 0.006222 |
| 786 | section_entropy_hash_43 | section | 0.1664 | 0.01723 |
| 1 298 | imports_function_hash_0099 | imports | 0.1623 | 0.002487 |
| 1 836 | imports_function_hash_0637 | imports | 0.1581 | 0.002775 |
| 2 054 | imports_function_hash_0855 | imports | 0.1579 | 0.0003926 |
| 2 372 | datadir_LOAD_CONFIG_TABLE_virtual_address | datadirectories | 0.1566 | 0.007536 |
| 2 359 | datadir_CERTIFICATE_TABLE_size | datadirectories | 0.1566 | 0.007541 |
| 2 371 | datadir_LOAD_CONFIG_TABLE_size | datadirectories | 0.1565 | 0.00552 |
| 623 | general_has_signature | general | 0.156 | 0.007296 |
| 2 360 | datadir_CERTIFICATE_TABLE_virtual_address | datadirectories | 0.1551 | 0.007543 |
| 595 | strings_printabledist_81 | strings | 0.1548 | 0.009241 |
| 590 | strings_printabledist_76 | strings | 0.1545 | 0.006886 |
| 1 679 | imports_function_hash_0480 | imports | 0.1534 | 0.005175 |
| 2 364 | datadir_DEBUG_virtual_address | datadirectories | 0.1532 | 0.01124 |
| 1 273 | imports_function_hash_0074 | imports | 0.1529 | 0.008911 |

Graf: `plots/drift_ks_by_group.png`; úplná tabuľka: `drift_ks.parquet`.

## 5. Mediány vybraných interpretovateľných príznakov
| časť | trieda | general_size | general_vsize | general_has_signature | general_imports | strings_entropy | section_num | header_coff_timestamp |
|---|---|---|---|---|---|---|---|---|
| train | benign | 1.343e+06 | 1.335e+06 | 1 | 181 | 6 | 5 | 1.633e+09 |
| train | malware | 6.67e+05 | 4.26e+05 | 0 | 84 | 6.138 | 4 | 1.384e+09 |
| validácia | benign | 1.343e+06 | 1.335e+06 | 1 | 183.5 | 6.001 | 5 | 1.634e+09 |
| validácia | malware | 6.715e+05 | 4.506e+05 | 0 | 87 | 6.144 | 4 | 1.384e+09 |
| test | benign | 1.949e+06 | 1.335e+06 | 1 | 261 | 6.013 | 5 | 1.642e+09 |
| test | malware | 7.803e+05 | 8.356e+05 | 0 | 113 | 6.3 | 4 | 1.437e+09 |

- `header_coff_timestamp` je čas zostavenia z hlavičky PE (dá sa ľahko sfalšovať); pri interpretácii modelov
  sledovať, či sa naň model neopiera ako na časový artefakt zberu dát.

## 6. Duplicity
- SHA-256 je v rámci datasetu unikátne (prekryv train/test vyriešený v indexe, pozri `processed/index/README.md`).
- Identické EMBER vektory pri rôznych SHA-256: 131 skupín,
  268 vzoriek; žiadna skupina neprechádza cez viac častí a žiadna nemá rozporné označenie.
