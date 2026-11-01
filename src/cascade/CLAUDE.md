# src/cascade/ – finálna kaskáda

Finálne usporiadanie, ktoré sa porovnáva s ostatnými prístupmi:

1. Ľahký statický študent (`models/students_static`) a ľahký dynamický študent (`models/students_dynamic`)
   ohodnotia vzorku.
2. Ak sa zhodnú na malware alebo benign, ich rozhodnutie je konečné.
3. Ak sa nezhodnú, vzorka ide veľkému hybridnému modelu (`models/hybrid`), ktorý rozhodne.

Tento priečinok obsahuje iba logiku kaskády: načíta už natrénované modely, spája ich rozhodnutia a meria
výpočtové nároky celého postupu. Modely sa tu netrénujú.

Otvorené (zatiaľ neurčené):
- ktorí študenti a ktorý hybridný model sa použijú,
- ako sa určia prahy študentov (na validácii),
- či sa kaskáda vyhodnocuje aj s vopred vypočítanými predikciami, alebo iba skutočným spustením modelov.
