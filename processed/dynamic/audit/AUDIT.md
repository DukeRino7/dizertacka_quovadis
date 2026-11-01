# Audit Speakeasy reportov

> Generované `src/data/audit_dynamic.py` (2026-11-01T19:32:20+01:00); časti: train, validation, test.
> Rozhodnutia o reprezentácii sa robia iba podľa tréningu; validácia a test sú popisné.
> Reporty pochádzajú z **emulácie Speakeasy**, nie z behu v plnohodnotnom Windows sandboxe.

## 1. Kompletnosť sťahovania (voči zoznamu súborov na Hugging Face)
- v zozname: 92406, na disku: 92406, chýba: 0
  {}, iná veľkosť než v zozname: 0
- vzoriek indexu bez reportu na disku: 0 

## 2. Stav načítania reportov
| status | test | train | validation |
|---|---|---|---|
| ok | 17339 | 66831 | 7426 |

## 3. Prehľad podľa časti a rodiny
| časť | rodina | n | API volaní medián [p5–p95] | malé (≤5 volaní) | bez API volaní | chyba v module_entry | limit 500 vo vstupnom bode | s vláknami | s udalosťami |
|---|---|---|---|---|---|---|---|---|---|
| train | backdoor | 9955 | 499 [102–501] | 0.003 | 0.000 | 0.694 | 0.462 | 0.006 | 0.655 |
| train | benign | 21974 | 188 [5–498] | 0.068 | 0.000 | 0.582 | 0.049 | 0.007 | 0.590 |
| train | coinminer | 5893 | 242 [68–500] | 0.005 | 0.000 | 0.749 | 0.113 | 0.000 | 0.522 |
| train | dropper | 7419 | 21 [2–443] | 0.226 | 0.000 | 0.474 | 0.021 | 0.007 | 0.468 |
| train | keylogger | 3539 | 226 [11–360] | 0.002 | 0.000 | 0.853 | 0.004 | 0.001 | 0.862 |
| train | ransomware | 8665 | 180 [2–423] | 0.420 | 0.000 | 0.259 | 0.024 | 0.029 | 0.048 |
| train | rat | 1527 | 214 [2–225] | 0.104 | 0.000 | 0.847 | 0.007 | 0.000 | 0.807 |
| train | trojan | 7859 | 93 [4–501] | 0.064 | 0.000 | 0.630 | 0.205 | 0.008 | 0.576 |
| validation | backdoor | 1106 | 499 [106–501] | 0.001 | 0.000 | 0.679 | 0.476 | 0.003 | 0.641 |
| validation | benign | 2442 | 187 [5–498] | 0.069 | 0.000 | 0.576 | 0.048 | 0.006 | 0.586 |
| validation | coinminer | 655 | 239 [68–500] | 0.005 | 0.000 | 0.769 | 0.125 | 0.000 | 0.544 |
| validation | dropper | 824 | 20 [2–472] | 0.235 | 0.000 | 0.458 | 0.021 | 0.002 | 0.470 |
| validation | keylogger | 393 | 226 [14–349] | 0.005 | 0.000 | 0.865 | 0.000 | 0.000 | 0.878 |
| validation | ransomware | 962 | 180 [2–423] | 0.417 | 0.000 | 0.257 | 0.022 | 0.032 | 0.046 |
| validation | rat | 170 | 220 [14–225] | 0.047 | 0.000 | 0.906 | 0.012 | 0.000 | 0.888 |
| validation | trojan | 874 | 93 [4–501] | 0.065 | 0.000 | 0.609 | 0.204 | 0.008 | 0.606 |
| test | backdoor | 1940 | 499 [8–501] | 0.031 | 0.000 | 0.763 | 0.417 | 0.004 | 0.395 |
| test | benign | 7940 | 172 [4–477] | 0.060 | 0.000 | 0.740 | 0.037 | 0.002 | 0.114 |
| test | coinminer | 1684 | 219 [23–479] | 0.005 | 0.000 | 0.780 | 0.014 | 0.001 | 0.199 |
| test | dropper | 252 | 22 [7–426] | 0.004 | 0.000 | 0.631 | 0.024 | 0.000 | 0.278 |
| test | keylogger | 1041 | 32 [6–234] | 0.012 | 0.000 | 0.822 | 0.000 | 0.001 | 0.692 |
| test | ransomware | 2139 | 142 [8–497] | 0.019 | 0.000 | 0.629 | 0.042 | 0.203 | 0.272 |
| test | rat | 1258 | 214 [9–219] | 0.007 | 0.000 | 0.781 | 0.002 | 0.000 | 0.131 |
| test | trojan | 1085 | 74 [5–190] | 0.051 | 0.000 | 0.748 | 0.016 | 0.009 | 0.375 |

## 4. Chyby emulácie v module_entry (najčastejšie)
| split | module_entry_error | n |
|---|---|---|
| test | unsupported_api | 9472 |
| test | max_api_count | 2128 |
| test | Invalid memory read (UC_ERR_READ_UNMAPPED) | 623 |
| test | invalid_read | 233 |
| test | invalid_fetch | 83 |
| test | Failed to get character width from function: KERNEL32.GetEnv | 63 |
| train | max_api_count | 13540 |
| train | Invalid memory read (UC_ERR_READ_UNMAPPED) | 12852 |
| train | Invalid memory fetch (UC_ERR_FETCH_UNMAPPED) | 5480 |
| train | invalid_fetch | 2757 |
| train | invalid_read | 2242 |
| train | Invalid memory write (UC_ERR_WRITE_UNMAPPED) | 706 |
| validation | max_api_count | 1496 |
| validation | Invalid memory read (UC_ERR_READ_UNMAPPED) | 1419 |
| validation | Invalid memory fetch (UC_ERR_FETCH_UNMAPPED) | 641 |
| validation | invalid_fetch | 296 |
| validation | invalid_read | 246 |
| validation | Invalid memory write (UC_ERR_WRITE_UNMAPPED) | 66 |

## 5. Malé reporty (≤ 5 API volaní) – najčastejšie začiatky postupnosti, iba tréning
| seq | backdoor | benign | coinminer | dropper | keylogger | ransomware | rat | trojan | spolu |
|---|---|---|---|---|---|---|---|---|---|
| kernel32.getsystemtimeasfiletime → kernel32.getcurrentthreadid → kernel32.getcurrentprocessid → kernel32.queryperformancecounter → kernel32.isprocessorfeaturepresent | 0 | 358 | 0 | 0 | 0 | 0 | 0 | 0 | 358 |
| msvcrt.__set_app_type → kernel32.setunhandledexceptionfilter → msvcrt.__getmainargs → msvcrt.__p__fmode → msvcrt.__p__environ | 2 | 220 | 25 | 56 | 0 | 0 | 0 | 36 | 339 |
| crtdll.__getmainargs → user32.getcursorinfo → iphlpapi.getadaptersinfo | 0 | 0 | 0 | 307 | 0 | 0 | 0 | 0 | 307 |
| kernel32.getcpinfo → advapi32.regopenkeyexw | 0 | 0 | 0 | 213 | 0 | 0 | 0 | 21 | 234 |
| kernel32.getuserdefaultuilanguage → kernel32.getuserdefaultuilanguage | 0 | 0 | 0 | 0 | 0 | 188 | 0 | 0 | 188 |
| kernel32.getconsolewindow → kernel32.getconsolewindow | 0 | 0 | 0 | 0 | 0 | 183 | 0 | 0 | 183 |
| kernel32.getcpinfo → kernel32.loadlibrarya → kernel32.getprocaddress → advapi32.regopenkeyexw | 0 | 0 | 0 | 142 | 0 | 0 | 0 | 27 | 169 |
| msvbvm60.ordinal_100 → msvbvm60.event_sink_release | 0 | 1 | 0 | 2 | 0 | 0 | 159 | 0 | 162 |
| crtdll.__getmainargs → crtdll._initterm | 0 | 11 | 0 | 0 | 0 | 0 | 0 | 80 | 91 |
| user32.getsystemmetrics → user32.getsystemmetrics → advapi32.regopenkeyexw | 0 | 0 | 0 | 91 | 0 | 0 | 0 | 0 | 91 |
| crtdll.__getmainargs → iphlpapi.getadaptersinfo | 0 | 0 | 0 | 87 | 0 | 0 | 0 | 0 | 87 |
| kernel32.getvolumeinformation → kernel32.getversionex | 0 | 0 | 0 | 0 | 0 | 85 | 0 | 0 | 85 |
| kernel32.getprofileintw → kernel32.getlongpathnamea → kernel32.getlongpathnamea | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 65 | 65 |
| kernel32.getsystemtimeasfiletime → kernel32.getcurrentthreadid → kernel32.getcurrentprocessid → kernel32.queryperformancecounter | 0 | 61 | 0 | 0 | 0 | 0 | 0 | 0 | 61 |
| crtdll.__getmainargs → crypt32.cryptbinarytostringa → kernel32.getlasterror | 0 | 0 | 0 | 58 | 0 | 0 | 0 | 0 | 58 |

Ak sa niektorá krátka postupnosť vyskytuje takmer iba v jednej rodine, je to **riziko skratky** – model by sa mohol
naučiť „krátky report = táto rodina“ namiesto správania.

## 6. Slovník API (tréning, názvy malými písmenami)
{'unique_api_train': 2722, 'api_in_>=_5_train_samples': 1099, 'api_in_>=_20_train_samples': 675, 'api_in_>=_100_train_samples': 422}; úplný zoznam: `api_vocabulary_train.csv`.

Grafy: `plots/tiny_reports_by_family.png`, `plots/api_calls_by_family.png`.
