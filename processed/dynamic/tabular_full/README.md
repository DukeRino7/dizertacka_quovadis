# processed/dynamic/tabular/ – dynamický dataset pre spoločný rebríček

> Generované `src/data/build_dynamic_tabular.py`. Štatistiky: [STATISTICS.md](STATISTICS.md).

## Použité techniky
1. Vstup: normalizovaná cache reportov (`processed/dynamic/cache`) – všetky vstupné body a vlákna vzorky spolu,
   názvy API malými písmenami; poradie vzoriek = spoločný index.
2. Reprezentácia: n-gramy postupnosti API volaní (rozsah (1, 2)), slovník z **tréningu**
   (min. 5 vzoriek, top 2000 podľa dokumentovej frekvencie); počty udalostí podľa typu;
   súhrnné príznaky reportu. Hodnoty = surové počty.
3. Učené transformácie modelov (log1p, štandardizácia) sa robia v experimente, ako pri statických dátach.
4. Neznáme n-gramy vo validácii/teste sa ignorujú (nevidené správanie nemá vlastný príznak).

## Obmedzenia
- Reporty pochádzajú z emulácie Speakeasy (limit 500 API volaní na vstupný bod, časový limit 60 s);
  veľká časť vstupných bodov končí chybou emulátora – pozri `processed/dynamic/audit/AUDIT.md`.
- Argumenty API volaní sa v tejto reprezentácii nepoužívajú (sú v cache pre špecifické modely vrstvy B).
