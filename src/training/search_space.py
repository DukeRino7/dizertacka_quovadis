"""Priestor hyperparametrov z YAML konfigurácie -> návrhy Optuna.

Formát v konfigurácii:
    search_space:
      C: {type: float, low: 1.0e-4, high: 100, log: true}
      max_depth: {type: categorical, choices: [16, 32, null]}
      n_estimators: {type: int, low: 100, high: 500, step: 50}
    fixed_params:
      max_iter: 2000
"""
import optuna


def suggest(trial: optuna.Trial, space: dict) -> dict:
    out = {}
    for name, spec in space.items():
        t = spec["type"]
        if t == "float":
            out[name] = trial.suggest_float(name, float(spec["low"]), float(spec["high"]), log=spec.get("log", False))
        elif t == "int":
            out[name] = trial.suggest_int(name, int(spec["low"]), int(spec["high"]), step=spec.get("step", 1),
                                          log=spec.get("log", False))
        elif t == "categorical":
            out[name] = trial.suggest_categorical(name, spec["choices"])
        else:
            raise ValueError(f"neznámy typ {t!r} pri {name}")
    return out
