"""Pevný vektor z behaviorálneho reportu pre spoločný rebríček modelov (vrstva A).

Reprezentácia (parametre v configs/data/dynamic.yaml, NÁVRH):
- n-gramy postupnosti API volaní celej vzorky (1-gramy = jednotlivé volania, 2-gramy = dvojice po sebe),
  slovník = najčastejšie n-gramy podľa dokumentovej frekvencie IBA na tréningu (min_doc_freq, max_features),
  hodnota = počet výskytov (log a škálovanie robí až predspracovanie modelu, ako pri statických dátach),
- počty udalostí (súbory, register, sieť, procesy, vytvorené súbory, výnimky) podľa typu – slovník z tréningu,
- súhrnné príznaky reportu (počet vstupných bodov, vlákien, volaní, chýb emulácie, ...).
Slovník sa učí iba na tréningu; validácia a test sa iba transformujú (neznáme n-gramy sa ignorujú).
"""
from collections import Counter

import numpy as np
import pandas as pd

SUMMARY_COLUMNS = ["n_entry_points", "n_threads", "n_api_calls", "n_api_unique", "n_api_module_entry",
                   "max_api_per_ep", "n_ep_errors", "n_events", "n_dynamic_code_segments"]


def ngrams(seq, n: int):
    return zip(*(seq[i:] for i in range(n))) if n > 1 else ((s,) for s in seq)


class ApiNgramVectorizer:
    def __init__(self, ngram_range=(1, 2), min_doc_freq=5, max_features=2000, count_transform="none",
                 include_events=True, include_summary=True):
        self.ngram_range = tuple(ngram_range)
        self.min_doc_freq = min_doc_freq
        self.max_features = max_features
        self.count_transform = count_transform
        self.include_events = include_events
        self.include_summary = include_summary

    def _grams(self, seq):
        out = Counter()
        for n in range(self.ngram_range[0], self.ngram_range[1] + 1):
            out.update(" → ".join(g) for g in ngrams(list(seq), n))
        return out

    def fit(self, df: pd.DataFrame) -> "ApiNgramVectorizer":
        """df = tréningová časť cache (stĺpce api_seq, events, súhrnné počty)."""
        doc = Counter()
        for seq in df["api_seq"]:
            doc.update(self._grams(seq).keys())
        kept = [(g, c) for g, c in doc.items() if c >= self.min_doc_freq]
        kept.sort(key=lambda x: (-x[1], x[0]))  # deterministické poradie
        self.vocab_ = {g: i for i, (g, _) in enumerate(kept[: self.max_features])}
        self.doc_freq_ = {g: c for g, c in kept[: self.max_features]}
        ev = Counter()
        for e in df["events"]:
            ev.update(set(e))
        self.event_vocab_ = {k: i for i, k in enumerate(sorted(ev))} if self.include_events else {}
        self.n_train_ = len(df)
        return self

    def feature_table(self) -> pd.DataFrame:
        rows = [(f"api: {g}", "api_1gram" if " → " not in g else f"api_{g.count(' → ') + 1}gram") for g in self.vocab_]
        rows += [(f"event: {k}", "event") for k in self.event_vocab_]
        if self.include_summary:
            rows += [(f"summary: {c}", "summary") for c in SUMMARY_COLUMNS]
        df = pd.DataFrame(rows, columns=["name", "group"])
        df.insert(0, "column", range(len(df)))
        return df

    def transform(self, df: pd.DataFrame, dtype=np.float32) -> np.ndarray:
        nv, ne = len(self.vocab_), len(self.event_vocab_)
        ns = len(SUMMARY_COLUMNS) if self.include_summary else 0
        X = np.zeros((len(df), nv + ne + ns), dtype=dtype)
        for i, seq in enumerate(df["api_seq"]):
            for g, c in self._grams(seq).items():
                j = self.vocab_.get(g)
                if j is not None:
                    X[i, j] = c
        if ne:
            for i, ev in enumerate(df["events"]):
                for k, c in Counter(ev).items():
                    j = self.event_vocab_.get(k)
                    if j is not None:
                        X[i, nv + j] = c
        if ns:
            X[:, nv + ne:] = df[SUMMARY_COLUMNS].to_numpy(dtype=dtype)
        if self.count_transform == "log1p":
            X = np.log1p(X)
        return X
