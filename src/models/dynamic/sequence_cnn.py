"""Sekvenčný model nad postupnosťou API volaní (vrstva B, dynamický prístup).

Vstup: ID tokenov API [n, max_len] (processed/dynamic/sequence, 0 = PAD). Architektúra: embedding API →
paralelné 1D konvolúcie s rôznymi šírkami okna (zachytia krátke vzory volaní) → maximum cez postupnosť
(maskované doplnenie) → plne prepojená hlava. Hyperparametre: configs/dynamic/seq_cnn.yaml.
"""
import numpy as np
import torch
from torch import nn

from src.models.torch_base import TorchModel


def parse_kernels(k) -> list[int]:
    """Šírky okien konvolúcií; v konfigurácii ako zoznam alebo reťazec '3-5-7' (Optuna nevie zoznamy)."""
    return [int(v) for v in k.split("-")] if isinstance(k, str) else [int(v) for v in k]


class SeqCNNNet(nn.Module):
    def __init__(self, vocab_size: int, emb_dim: int, channels: int, kernels: list[int], hidden: int, dropout: float):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, emb_dim, padding_idx=0)
        self.convs = nn.ModuleList([nn.Conv1d(emb_dim, channels, k, padding=k // 2) for k in kernels])
        self.head = nn.Sequential(nn.Dropout(dropout), nn.Linear(channels * len(kernels), hidden), nn.ReLU(),
                                  nn.Dropout(dropout), nn.Linear(hidden, 1))
        self.out_dim = channels * len(kernels)

    def encode(self, tokens: torch.Tensor) -> torch.Tensor:
        mask = (tokens > 0).unsqueeze(1)                       # [b, 1, L]
        x = self.emb(tokens).transpose(1, 2)                   # [b, E, L]
        feats = []
        for conv in self.convs:
            h = torch.relu(conv(x))[..., : tokens.shape[1]]
            h = h.masked_fill(~mask, float("-inf")).amax(dim=2)
            feats.append(torch.nan_to_num(h, neginf=0.0))      # prázdna postupnosť -> 0
        return torch.cat(feats, dim=1)

    def forward(self, tokens):
        return self.head(self.encode(tokens)).squeeze(-1)


class SequenceCNN(TorchModel):
    name = "seq_cnn"

    def prepare_fit(self, X):
        self.vocab_size = int(np.max(X)) + 1 if self.params.get("vocab_size") is None else self.params["vocab_size"]

    def to_tensor(self, X, device):
        return torch.as_tensor(np.ascontiguousarray(X), dtype=torch.long, device=device).clamp_(0, self.vocab_size - 1)

    def build_net(self, X):
        p = self.params
        return SeqCNNNet(self.vocab_size, p["emb_dim"], p["channels"], parse_kernels(p["kernels"]), p["hidden"], p["dropout"])

    def meta(self):
        return {"vocab_size": self.vocab_size}

    def restore_meta(self, meta):
        self.vocab_size = meta["vocab_size"]
