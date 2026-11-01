"""Dvojvetvová hybridná sieť (vrstva B) – kandidát na veľký hybridný model v kaskáde.

Vstup (providers 'hybrid_seq'): [EMBER príznaky (n_static) | ID tokenov API (max_len)] v jednom poli float32.
- statická vetva: StaticPreprocessor (fit iba na tréningu) → MLP,
- dynamická vetva: embedding API → 1D konvolúcie → maximum cez postupnosť (ako SequenceCNN),
- spojenie oboch reprezentácií → plne prepojená hlava (stredná fúzia).
"""
from pathlib import Path

import joblib
import numpy as np
import torch
from torch import nn

from src.data.static_transforms import StaticPreprocessor
from src.models.dynamic.sequence_cnn import SeqCNNNet, parse_kernels
from src.models.torch_base import TorchModel


class TwoBranchNet(nn.Module):
    def __init__(self, n_static: int, static_widths: list[int], vocab_size: int, emb_dim: int, channels: int,
                 kernels: list[int], hidden: int, dropout: float):
        super().__init__()
        layers, prev = [], n_static
        for w in static_widths:
            layers += [nn.Linear(prev, w), nn.BatchNorm1d(w), nn.ReLU(), nn.Dropout(dropout)]
            prev = w
        self.static = nn.Sequential(*layers)
        self.seq = SeqCNNNet(vocab_size, emb_dim, channels, kernels, hidden, dropout)
        self.n_static = n_static
        self.head = nn.Sequential(nn.Linear(prev + self.seq.out_dim, hidden), nn.ReLU(), nn.Dropout(dropout),
                                  nn.Linear(hidden, 1))

    def forward(self, x):
        s = self.static(x[:, : self.n_static])
        d = self.seq.encode(x[:, self.n_static:].long())
        return self.head(torch.cat([s, d], dim=1)).squeeze(-1)


class TwoBranchHybrid(TorchModel):
    name = "two_branch"

    def prepare_fit(self, X):
        ns = self.params["n_static"]
        self.pre = StaticPreprocessor().fit(X[:, :ns])
        self.n_static_kept = int(self.pre.keep_.sum())
        self.vocab_size = int(np.max(X[:, ns:])) + 1

    def to_tensor(self, X, device):
        ns = self.params["n_static"]
        Z = np.hstack([self.pre.transform(X[:, :ns]), np.clip(X[:, ns:], 0, self.vocab_size - 1)]).astype(np.float32)
        return torch.as_tensor(Z, device=device)

    def build_net(self, X):
        p = self.params
        widths = [int(p["static_width"] * p.get("width_decay", 0.5) ** i) for i in range(p["static_layers"])]
        return TwoBranchNet(self.n_static_kept, widths, self.vocab_size, p["emb_dim"], p["channels"], parse_kernels(p["kernels"]),
                            p["hidden"], p["dropout"])

    def meta(self):
        return {"vocab_size": self.vocab_size, "n_static_kept": self.n_static_kept}

    def restore_meta(self, meta):
        self.vocab_size, self.n_static_kept = meta["vocab_size"], meta["n_static_kept"]

    def _save(self, path: Path):
        super()._save(path)
        joblib.dump(self.pre, path / "static_preprocessor.joblib")

    @classmethod
    def _load(cls, path, meta):
        m = cls(meta["params"], meta["seed"])
        m.restore_meta(meta)
        m.pre = joblib.load(path / "static_preprocessor.joblib")
        m.net = m.build_net(None)
        m.net.load_state_dict(torch.load(path / "model.pt", map_location="cpu"))
        return m
