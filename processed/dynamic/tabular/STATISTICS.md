# Štatistiky dynamického tabuľkového datasetu

> Generované `src/data/build_dynamic_tabular.py` (2026-11-01T19:51:20+01:00). Slovník a štatistiky príznakov iba z tréningu;
> porovnania s validáciou a testom sú popisné.

## Rozmery
| časť | vzorky | príznaky |
|---|---|---|
| train | 66831 | 2000 |
| validation | 7426 | 2000 |
| test | 17339 | 2000 |

## Skupiny príznakov (tréning)
| group | počet | konštantné | medián_podielu_nenulových |
|---|---|---|---|
| api_1gram | 449 | 0 | 0.009 |
| api_2gram | 1551 | 0 | 0.008 |

Slovník: 2000 n-gramov API (min. 5 tréningových vzoriek, max. 2000),
0 typov udalostí, súhrnné príznaky: nie.

## N-gramy s najväčším rozdielom výskytu medzi triedami (tréning, podiel vzoriek s n-gramom)
| name | benign | malware | rozdiel |
|---|---|---|---|
| api: kernel32.queryperformancecounter → kernel32.isprocessorfeaturepresent | 0.494 | 0.011 | -0.484 |
| api: kernel32.loadlibraryexw | 0.454 | 0.018 | -0.436 |
| api: kernel32.getprocaddress → kernel32.flsalloc | 0.442 | 0.012 | -0.430 |
| api: kernel32.loadlibraryexw → kernel32.getprocaddress | 0.440 | 0.010 | -0.430 |
| api: kernel32.getprocaddress → kernel32.flssetvalue | 0.439 | 0.010 | -0.429 |
| api: kernel32.flssetvalue → kernel32.loadlibraryexw | 0.436 | 0.009 | -0.427 |
| api: kernel32.getlasterror → kernel32.getprocaddress | 0.431 | 0.009 | -0.422 |
| api: kernel32.getprocessheap → kernel32.loadlibraryexw | 0.429 | 0.008 | -0.421 |
| api: kernel32.getprocaddress → kernel32.flsgetvalue | 0.429 | 0.008 | -0.421 |
| api: kernel32.flsalloc → kernel32.getlasterror | 0.430 | 0.010 | -0.420 |
| api: kernel32.initializecriticalsectionex → kernel32.getprocessheap | 0.429 | 0.010 | -0.420 |
| api: kernel32.isprocessorfeaturepresent → kernel32.loadlibraryexw | 0.420 | 0.009 | -0.410 |
| api: kernel32.getsystemtimeasfiletime → kernel32.getcurrentthreadid | 0.529 | 0.120 | -0.409 |
| api: kernel32.initializecriticalsectionex → kernel32.loadlibraryexw | 0.418 | 0.010 | -0.408 |
| api: kernel32.flsalloc → kernel32.getprocaddress | 0.418 | 0.010 | -0.407 |
| api: kernel32.getcurrentthreadid → kernel32.getcurrentprocessid | 0.527 | 0.120 | -0.406 |
| api: kernel32.getcurrentprocessid → kernel32.queryperformancecounter | 0.526 | 0.120 | -0.405 |
| api: kernel32.leavecriticalsection → kernel32.setlasterror | 0.409 | 0.010 | -0.399 |
| api: kernel32.heapalloc → kernel32.initializecriticalsectionex | 0.407 | 0.010 | -0.397 |
| api: kernel32.leavecriticalsection → kernel32.getacp | 0.402 | 0.010 | -0.392 |

## Posun rozdelenia príznakov (KS, popisné)
| group | KS train–val (medián) | KS train–test (medián) |
|---|---|---|
| api_1gram | 0.001 | 0.008 |
| api_2gram | 0.001 | 0.005 |
