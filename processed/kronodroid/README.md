# KronoDroid – pripravené dáta (V4)

> Generované `src/data/kronodroid/build_kronodroid.py` (2026-11-22T16:16:32+01:00). Plán: `docs/19_plan_v4.md`.

- vyradené SHA-256 s oboma označeniami: 4; súbory zariadenia: 78129, prekrytie s emulátorom: 63316
- statika: 173 oprávnení + 11 metadát (bez ['FilesInsideAPK']) + meta_missing = 185 príznakov;
  metadáta doplnené z emulátora v 264 súboroch, stále chýbajú v 379
- dynamika: 289 stĺpcov (systémové volania + nr_syscalls); D-norm: 288 podielov
- rodiny malvéru s < 50 vzorkami -> 'other' (184 rodín), bez rodiny -> 'unknown'
- skupiny identických statických vektorov: 74286

## Hlavné rozdelenie (real_full; real_p a emu_p sú jeho podmnožina)
| split | benign | malware |
|---|---|---|
| test | 7350 | 8275 |
| train | 25726 | 28964 |
| validation | 3675 | 4139 |

### Prekrytie (real_p, emu_p)
| split | benign | malware |
|---|---|---|
| test | 6983 | 5673 |
| train | 24505 | 19831 |
| validation | 3489 | 2835 |

## Doplnkový časový posun malvéru (real_time): test = malvér od roku 2015
| split_time | benign | malware |
|---|---|---|
| excluded | 0 | 448 |
| test | 7350 | 13471 |
| train | 25726 | 24035 |
| validation | 3675 | 3424 |

## Vynechávané rodiny (zero-day)
| rodina | real_full | prekrytie |
|---|---|---|
| Airpush/StopSMS | 7775 | 6507 |
| Boxer | 3597 | 3538 |
| FakeInst | 2384 | 2121 |
| Locker/SLocker Ransomware | 1846 | 1697 |
| BankBot | 1297 | 1230 |
