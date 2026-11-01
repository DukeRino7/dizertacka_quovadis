# src/evaluation/ – vyhodnotenie

Plánovaný obsah (zatiaľ neimplementované):
- **Detekčné metriky:** napr. accuracy, precision, recall, F1, ROC-AUC, PR-AUC, TPR pri pevnom FPR, matica zámen;
  aj rozpad podľa rodín malvéru.
- **Výpočtové nároky:** čas inferencie na vzorku a na dávku, priepustnosť, pamäť, veľkosť modelu, počet parametrov;
  zvlášť príprava priznakov, tréning a inferencia; zvlášť CPU a GPU.
- **Kaskáda:** podiel eskalácií, spoločné chyby pri zhode študentov, prínos veľkého modelu pri nezhode.
- **Grafy:** napr. ROC a PR krivky, matica zámen, porovnanie kvality voči času inferencie.

Grafy a metriky jedného modelu sa ukladajú do jeho behu v `runs/<prístup>/<model>/`,
porovnania viacerých prístupov do `runs/comparison/`.
