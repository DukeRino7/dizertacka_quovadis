# processed/dynamic/sequence/ – postupnosti API volaní pre sekvenčné modely

> Generované `src/data/build_dynamic_sequence.py` (2026-11-01T19:52:22+01:00).

- Slovník z **tréningu**: 1099 API (min. 5 vzoriek, max. 20000) + PAD (0) a UNK (1).
- Vzorka = prvých 1024 volaní celej postupnosti (všetky vstupné body a vlákna v poradí reportu), názvy malými písmenami.

| časť | vzorky | orezané (> max_len) | medián dĺžky | podiel UNK tokenov |
|---|---|---|---|---|
| train | 66831 | 0.0013 | 181 | 0.0005 |
| validation | 7426 | 0.0009 | 187 | 0.0003 |
| test | 17339 | 0.0001 | 175 | 0.0005 |
