# processed/index/ – spoločný index vzoriek a rozdelenie

> Automaticky generované skriptom `src/data/build_index.py` (2026-11-01T13:35:33+01:00).
> Konfigurácia: `configs/data/index.yaml`. Neupravovať ručne – pri zmene spustiť skript znova.

Tento index a rozdelenie používajú **všetky** modely (statické, dynamické, hybridné, študenti, kaskáda).
Vzorka = jeden PE súbor identifikovaný SHA-256.

## Súbory
| Súbor | Obsah |
|---|---|
| `samples.parquet` | použité vzorky: `sha256`, `family`, `label` (0 benign / 1 malware), `original_split`, `split`, `feature_group`, `ember_file`, `ember_row`, `speakeasy_path`, `speakeasy_bytes` |
| `excluded.parquet` | vyradené vzorky s dôvodom |
| `ember_errors.parquet` | súbory bez EMBER príznakov (zlyhaná extrakcia v pôvodnom datasete) |
| `manifest.json` | konfigurácia, commit, prostredie, kontrolné súčty vstupov a výstupov |

## Postup
1. Načítanie katalógu EMBER s kontrolou integrity (indexy, nulové riadky zlyhaných extrakcií, platnosť SHA-256).
   Riadok matice sa určuje indexom z `hashes.txt`.
2. Vynechanie 366 súborov so zlyhanou extrakciou EMBER (príznaky neexistujú).
3. Prekryv pôvodného train/test podľa SHA-256: politika `drop_from_train`,
   vyradených 446 záznamov.
4. Zoskupenie vzoriek s identickým EMBER vektorom (MD5 bajtov vektora → `feature_group`).
5. Vyčlenenie validácie z pôvodného tréningu: `StratifiedGroupKFold`, 10 častí,
   jedna časť = validácia (podiel 0.1), stratifikácia podľa `family`,
   skupiny identických vektorov vždy spolu, seed 42.
   Pôvodný test zostáva bez zmeny (časový posun: tréning január 2022, test apríl 2022).
6. Priradenie Speakeasy reportu podľa SHA-256 (zo zoznamu súborov na Hugging Face).

## Počty podľa rodiny a časti
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

## Binárne označenie
| časť | benign (0) | malware (1) | podiel malware |
|---|---|---|---|
| train | 21 974 | 44 857 | 0.671 |
| validation | 2 442 | 4 984 | 0.671 |
| test | 7 940 | 9 399 | 0.542 |

## Kontroly
- Unikátne SHA-256 v indexe: True
- Vzorky so Speakeasy reportom v zozname súborov: 91596 z 91596
- Zhoda rodiny EMBER vs. Speakeasy priečinok: 91596 z 91596
- Skupiny identických EMBER vektorov s viac ako 1 vzorkou: 131
  (vzoriek v nich: 268);
  skupiny cez viac častí rozdelenia: 0;
  skupiny s rozporným označením: 0

## Rozhodnutia označené ako NÁVRH (neschválené)
- veľkosť validácie (0.1),
- politika prekryvu train/test (`drop_from_train`).
Zmena = úprava `configs/data/index.yaml` a nové spustenie skriptu.
