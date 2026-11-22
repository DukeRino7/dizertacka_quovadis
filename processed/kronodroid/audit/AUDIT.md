# Audit KronoDroid

> Generované `src/data/kronodroid/audit_kronodroid.py` (2026-11-22T15:32:04+01:00). Iba popis, rozhodnutia patria do docs/18.
> Zdroj https://github.com/aleguma/kronodroid (commit `c6ec342`), ZIP súbory sedia s konfiguráciou: True.

## 1. Základ
| | emulátor | skutočné zariadenie |
|---|---|---|
| riadky | 63991 | 78137 |
| benign / malware | 35246 / 28745 | 36755 / 41382 |
| označenie sedí so súborom | 63991 | 78137 |
| platné SHA-256 / unikátne | 63991 / 63987 | 78137 / 78133 |
| SHA-256 v oboch triedach | 4 | 4 |
| dynamické stĺpce (systémové volania vrátane nr_syscalls) | 289 | 289 |
| oprávnenia a ich súčty | 173 | 173 |
| statické metadáta (počty komponentov, veľkosť) | 12 | 12 |
| chýbajúce metadáta | [] | [] |
| nr_syscalls = 0 | 94 | 471 |
| nr_syscalls = súčet volaní | 63991 | 78137 |
| medián nr_syscalls benign / malware | 2958 / 2363 | 1148 / 3258 |
| rodiny malvéru | 209 | 240 |
| malvér bez rodiny | 91 | 165 |
| **benign s vyplnenou rodinou** | 2765 | 2959 |
| unikátne názvy balíkov | 48172 | 60082 |

Chýbajúce hodnoty (stĺpec: počet): emulátor {'FilesInsideAPK': 28745, 'Activities': 309, 'NrIntServices': 309, 'NrIntServicesActions': 309, 'NrIntActivities': 309, 'NrIntActivitiesActions': 309, 'NrIntReceivers': 309, 'NrIntReceiversActions': 309, 'TotalIntentFilters': 310, 'NrServices': 309, 'MalFamily': 32572}; zariadenie {'Activities': 642, 'NrIntServices': 642, 'NrIntServicesActions': 642, 'NrIntActivities': 642, 'NrIntActivitiesActions': 642, 'NrIntReceivers': 642, 'NrIntReceiversActions': 642, 'TotalIntentFilters': 643, 'NrServices': 642, 'MalFamily': 33961}.

## 2. Duplicity
| | emulátor | skutočné zariadenie |
|---|---|---|
| duplicitné riadky vo všetkých príznakoch | 167 | 171 |
| duplicitné riadky v statických príznakoch | 2545 | 3837 |
| unikátne statické vektory | 61446 | 74300 |
| duplicitné riadky iba v oprávneniach | 53128 | 64424 |
| skupiny rovnakých príznakov s oboma triedami | 0 | 0 |

## 3. Prekrytie emulátora a skutočného zariadenia (SHA-256)
- v oboch: **63320** (benign/malware {0: 34981, 1: 28339}), iba emulátor 667, iba zariadenie 14813
- zhodné označenie 63320, zhodné statické príznaky 34749, zhodná rodina 61443, zhodný dátum 63320
- rovnaké dynamické stĺpce: True; úplne zhodné dynamické vektory 38
- medián nr_syscalls na prekrytí: emulátor 2740, zariadenie 1407; Spearman 0.617

## 4. Stĺpce z VirusTotal (podobné označeniu)
Detection_Ratio podľa triedy: emulátor {'0': {'min': 0.0, 'median': 0.0, 'max': 0.538, 'share_gt0': 0.1259}, '1': {'min': 0.0, 'median': 0.47, 'max': 0.91, 'share_gt0': 0.9983}}; zariadenie {'0': {'min': 0.0, 'median': 0.0, 'max': 0.545, 'share_gt0': 0.1321}, '1': {'min': 0.0, 'median': 0.477, 'max': 0.91, 'share_gt0': 0.9979}}.

## 5. Dátumy (dátumy súborov vo vnútri APK, nie prvé objavenie)
emulátor {'date_first': {'unparsed': 1312, 'year_1980': 5285, 'before_2008': 5725, 'after_2020': 0, 'min': '1980-01-01', 'max': '2020-12-14'}, 'date_last': {'unparsed': 1199, 'year_1980': 23, 'before_2008': 57, 'after_2020': 5, 'min': '1980-01-01', 'max': '2107-11-30'}}

zariadenie {'date_first': {'unparsed': 1513, 'year_1980': 6945, 'before_2008': 7446, 'after_2020': 2, 'min': '1980-01-01', 'max': '2107-11-30'}, 'date_last': {'unparsed': 1357, 'year_1980': 24, 'before_2008': 57, 'after_2020': 7, 'min': '1980-01-01', 'max': '2107-11-30'}}

### Roky podľa triedy (date_last), emulátor
| date_last_dt | benign | malware |
|---|---|---|
| 2008 | 66 | 713 |
| 2009 | 609 | 19 |
| 2010 | 4981 | 260 |
| 2011 | 22149 | 2277 |
| 2012 | 310 | 6499 |
| 2013 | 444 | 5641 |
| 2014 | 596 | 6291 |
| 2015 | 689 | 1053 |
| 2016 | 715 | 1958 |
| 2017 | 626 | 808 |
| 2018 | 737 | 2435 |
| 2019 | 1403 | 185 |
| 2020 | 1010 | 256 |

### Roky podľa triedy (date_last), skutočné zariadenie
| date_last_dt | benign | malware |
|---|---|---|
| 2008 | 64 | 968 |
| 2009 | 623 | 20 |
| 2010 | 5084 | 269 |
| 2011 | 23089 | 3137 |
| 2012 | 342 | 7567 |
| 2013 | 489 | 7490 |
| 2014 | 632 | 8015 |
| 2015 | 721 | 1450 |
| 2016 | 743 | 2485 |
| 2017 | 652 | 4861 |
| 2018 | 780 | 4184 |
| 2019 | 1507 | 209 |
| 2020 | 1056 | 279 |

## 6. Rodiny
Počet rodín s aspoň N vzorkami: emulátor {50: 49, 100: 27, 500: 11, 1000: 8}; zariadenie {50: 57, 100: 36, 500: 14, 1000: 9}.

### Najčastejšie rodiny, skutočné zariadenie
| MalFamily | počet |
|---|---|
| Airpush/StopSMS | 7775 |
| SMSreg | 5019 |
| Malap | 4055 |
| Boxer | 3597 |
| Agent | 2934 |
| FakeInst | 2384 |
| Locker/SLocker Ransomware | 1846 |
| BankBot | 1297 |
| Dowgin | 1145 |
| FakeApp | 994 |
| DroidKungFu | 990 |
| Kuguo | 843 |
| GinMaster | 827 |
| Youmi | 628 |
| Waps/Simhosy | 399 |
