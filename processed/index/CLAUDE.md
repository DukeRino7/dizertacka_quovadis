# processed/index/ – spoločný index a rozdelenie

Popis, postup a počty: `README.md` (generovaný). Vytvára `src/data/build_index.py`, konfigurácia `configs/data/index.yaml`.
Rozdelenie je spoločné pre **všetky** modely – nemeniť ho medzi experimentmi. Pri zmene konfigurácie treba
znovu vytvoriť aj `processed/static` (a neskôr dynamické dáta) a všetky dovtedajšie výsledky v `runs/` sú neplatné.
