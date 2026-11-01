"""Viacvrstvový perceptrón (PyTorch). Malé aj veľké MLP sú ten istý model s iným priestorom hyperparametrov.

Učenie: AdamW, vážená binárna krížová entropia, early stopping podľa ROC-AUC na validácii
(obnoví sa najlepšia epocha), zníženie learning rate pri stagnácii.
"""
import copy
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from torch import nn

from .base import TabularModel

_TENSOR_CACHE: dict = {}


def _to_tensor(X, device):
    key = (id(X), len(X), device)
    if key not in _TENSOR_CACHE:
        if len(_TENSOR_CACHE) > 4:
            _TENSOR_CACHE.clear()
        _TENSOR_CACHE[key] = torch.as_tensor(np.ascontiguousarray(X), dtype=torch.float32, device=device)
    return _TENSOR_CACHE[key]


def layer_widths(p: dict) -> list[int]:
    w, out = p["hidden_width"], []
    for _ in range(p["hidden_layers"]):
        out.append(max(int(w), 16))
        w *= p.get("width_decay", 1.0)
    return out


class MLPNet(nn.Module):
    def __init__(self, n_in: int, widths: list[int], dropout: float):
        super().__init__()
        layers, prev = [], n_in
        for w in widths:
            layers += [nn.Linear(prev, w), nn.BatchNorm1d(w), nn.ReLU(), nn.Dropout(dropout)]
            prev = w
        layers.append(nn.Linear(prev, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x).squeeze(-1)


class MLP(TabularModel):
    name = "mlp"
    needs_scaling = True
    supports_gpu = True

    def __init__(self, params, seed, threads=-1):
        super().__init__(params, seed, threads)
        self.device = "cpu"

    def fit(self, X, y, w, X_val, y_val):
        p = self.params
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        torch.manual_seed(self.seed)
        self.n_in = X.shape[1]
        self.net = MLPNet(self.n_in, layer_widths(p), p["dropout"]).to(dev)
        opt = torch.optim.AdamW(self.net.parameters(), lr=p["lr"], weight_decay=p["weight_decay"])
        sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, mode="max", factor=0.5, patience=p.get("lr_patience", 3))
        loss_fn = nn.BCEWithLogitsLoss(reduction="none")
        Xt, yt = _to_tensor(X, dev), torch.as_tensor(y, dtype=torch.float32, device=dev)
        wt = torch.as_tensor(w, dtype=torch.float32, device=dev)
        Xv = _to_tensor(X_val, dev)
        gen = torch.Generator(device=dev).manual_seed(self.seed)
        bs, best, best_state, bad, hist = p["batch_size"], -1.0, None, 0, {"train_loss": [], "validation_auc": []}
        for epoch in range(p.get("max_epochs", 100)):
            self.net.train()
            perm = torch.randperm(len(Xt), device=dev, generator=gen)
            total = 0.0
            for i in range(0, len(perm), bs):
                b = perm[i:i + bs]
                if len(b) < 2:
                    continue
                opt.zero_grad(set_to_none=True)
                loss = (loss_fn(self.net(Xt[b]), yt[b]) * wt[b]).sum() / wt[b].sum()
                loss.backward()
                opt.step()
                total += loss.item() * len(b)
            auc = roc_auc_score(y_val, self._predict_tensor(Xv))
            hist["train_loss"].append(total / len(perm)); hist["validation_auc"].append(auc)
            sched.step(auc)
            if auc > best + 1e-5:
                best, best_state, bad = auc, copy.deepcopy(self.net.state_dict()), 0
            else:
                bad += 1
                if bad >= p.get("patience", 8):
                    break
        self.net.load_state_dict(best_state)
        self.best_epoch = int(np.argmax(hist["validation_auc"])) + 1
        self.to_device("cpu")
        torch.cuda.empty_cache()
        return {"best_epoch": self.best_epoch, **hist}

    @torch.no_grad()
    def _predict_tensor(self, Xt, bs: int = 8192) -> np.ndarray:
        self.net.eval()
        return np.concatenate([torch.sigmoid(self.net(Xt[i:i + bs])).float().cpu().numpy()
                               for i in range(0, len(Xt), bs)])

    def predict_proba(self, X):
        Xt = torch.as_tensor(np.ascontiguousarray(X), dtype=torch.float32, device=self.device)
        return self._predict_tensor(Xt)

    def set_threads(self, n):
        self.threads = n
        torch.set_num_threads(max(n, 1))

    def to_device(self, dev):
        self.device = dev
        self.net.to(dev)

    def n_parameters(self):
        return int(sum(p.numel() for p in self.net.parameters()))

    def _extra_meta(self):
        return {"n_in": self.n_in, "widths": layer_widths(self.params), "best_epoch": getattr(self, "best_epoch", None)}

    def _save(self, path: Path):
        torch.save(self.net.state_dict(), path / "model.pt")

    @classmethod
    def _load(cls, path, meta):
        m = cls(meta["params"], meta["seed"])
        m.n_in = meta["n_in"]
        m.net = MLPNet(m.n_in, meta["widths"], meta["params"]["dropout"])
        m.net.load_state_dict(torch.load(path / "model.pt", map_location="cpu"))
        return m
