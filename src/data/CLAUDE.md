# src/data/ – príprava dát

Jediné miesto, ktoré číta surové dáta z `data/`. Ostatný kód pracuje s výstupmi v `processed/`.

Plánované kroky (zatiaľ neimplementované):
1. **Audit** – reprodukovateľné overenie štruktúry, počtov, párovania a problémov (výsledky v `docs/01_audit_dat.md`).
2. **Spoločný index** – jeden riadok na vzorku (SHA-256): pôvodná časť, rodina, binárne označenie, cesty k zdrojom.
3. **Rozdelenie** – zachovaný pôvodný test, validácia vyčlenená z tréningu, pevný seed; rovnaké pre všetky modely.
4. **Cache EMBER** – matica zoradená podľa indexu.
5. **Cache Speakeasy** – po dokončení sťahovania; jedna vzorka = jeden súbor so všetkými vstupnými bodmi a vláknami.
6. **Načítanie** – funkcie, ktoré modelom vrátia dáta pre zvolenú časť rozdelenia.

Overené úskalia (detaily v `docs/01_audit_dat.md`):
- V EMBER `features.npy` sa riadok vzorky určuje **indexom z prvého stĺpca `hashes.txt`**, nie poradím riadku.
  Riadky zlyhaných extrakcií sú v matici nulové.
- Speakeasy: SHA-256 je iba v názve súboru, v traine `sha.json`, v teste `sha.dat.json`;
  train `report_backdoor` a `report_clean` majú ďalšiu úroveň podpriečinkov.
- 446 SHA-256 je v traine aj teste (keylogger). Riešenie zatiaľ nie je schválené.
