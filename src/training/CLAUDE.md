# src/training/ – trénovanie a destilácia

- Spoločný trénovací postup pre modely, ktoré ho potrebujú (napr. neurónové siete).
- Destilácia vedomostí: učiteľ → študent. Spôsob destilácie zatiaľ **nie je určený**.

Pravidlá:
- Všetky učené transformácie a destilácia iba na tréningovej časti.
- Validácia slúži na výber hyperparametrov, prahov a zastavenie tréningu. Test sa tu nepoužíva.
- Čas tréningu sa meria a ukladá samostatne od inferencie a prípravy priznakov.
