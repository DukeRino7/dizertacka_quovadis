# processed/ – predspracované dáta (cache)

Odvodené dáta vytvorené kódom zo `src/data`, aby sa surové dáta nespracovávali pri každom behu.

Pravidlá:
- Všetko tu musí byť **znovu vytvoriteľné** spustením skriptu zo `src/data` (priečinok sa necommituje do gitu).
- Každý výstup má vedľa seba metadáta: ktorý skript a konfigurácia ho vytvorili, kedy a z akých vstupov.
- Ucené transformácie (napr. normalizácia, slovník API volaní) sa sem **neukladajú**. Fitujú sa iba na
  tréningu v rámci konkrétneho experimentu a ukladajú sa do jeho priečinka v `runs/`.

Návrh obsahu (zatiaľ nevytvorené):
- `index/` – spoločný index vzoriek (sha256, pôvodná časť, rodina, binárne označenie, cesty k zdrojom)
  a pevné rozdelenie train/validation/test zdieľané všetkými modelmi.
- `ember/` – EMBER matica zoradená podľa indexu (napr. jeden `.npy` súbor na mmap).
- `speakeasy/` – reporty zredukované na formu vhodnú pre modely (presný formát sa určí neskôr).
