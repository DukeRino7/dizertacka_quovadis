"""Spoločný tréningový cyklus pre neurónové modely vrstvy B (sekvenčná CNN, dvojvetvová sieť).

Rovnaké pravidlá ako MLP v rebríčku: AdamW, vážená binárna krížová entropia, early stopping podľa ROC-AUC
na validácii s obnovou najlepšej epochy, zníženie learning rate pri stagnácii. Rozhranie = TabularModel,
takže funguje rovnaký spúšťač, benchmark aj porovnanie.
"""
import copy
from abc import abstractmethod
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from torch import nn

from src.models.tabular.base import TabularModel


class TorchModel(TabularModel):
    supports_gpu = True
    predict_batch = 512  # menšie dávky – konvolúcie nad dlhými postupnosťami sú pamäťovo náročné

    def __init__(self, params, seed, threads=-1):
        super().__init__(params, seed, threads)
        self.device = "cpu"

    # --- hooky pre konkrétny model -------------------------------------------------------------
    @abstractmethod
    def build_net(self, X: np.ndarray) -> nn.Module:
        """Vytvorí sieť; smie si z tréningových X zapamätať potrebné rozmery (veľkosť slovníka, ...)."""

    def prepare_fit(self, X: np.ndarray) -> None:
        """Voliteľne: učené transformácie vstupu (iba z tréningových X)."""

    def to_tensor(self, X: np.ndarray, device) -> torch.Tensor:
        return torch.as_tensor(np.ascontiguousarray(X), dtype=torch.float32, device=device)

    @abstractmethod
    def meta(self) -> dict: ...

    # --- tréning -------------------------------------------------------------------------------
    def fit(self, X, y, w, X_val, y_val):
        p = self.params
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        torch.manual_seed(self.seed)
        self.prepare_fit(X)
        self.net = self.build_net(X).to(dev)
        opt = torch.optim.AdamW(self.net.parameters(), lr=p["lr"], weight_decay=p["weight_decay"])
        sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, mode="max", factor=0.5, patience=p.get("lr_patience", 2))
        loss_fn = nn.BCEWithLogitsLoss(reduction="none")
        Xt, Xv = self.to_tensor(X, dev), self.to_tensor(X_val, dev)
        yt = torch.as_tensor(y, dtype=torch.float32, device=dev)
        wt = torch.as_tensor(w, dtype=torch.float32, device=dev)
        gen = torch.Generator(device=dev).manual_seed(self.seed)
        bs, best, best_state, bad = p["batch_size"], -1.0, None, 0
        hist = {"train_loss": [], "validation_auc": []}
        for _ in range(p.get("max_epochs", 30)):
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
                nn.utils.clip_grad_norm_(self.net.parameters(), 5.0)
                opt.step()
                total += loss.item() * len(b)
            auc = roc_auc_score(y_val, self._predict_tensor(Xv))
            hist["train_loss"].append(total / len(perm)); hist["validation_auc"].append(auc)
            sched.step(auc)
            if auc > best + 1e-5:
                best, best_state, bad = auc, copy.deepcopy(self.net.state_dict()), 0
            else:
                bad += 1
                if bad >= p.get("patience", 4):
                    break
        self.net.load_state_dict(best_state)
        self.best_epoch = int(np.argmax(hist["validation_auc"])) + 1
        del Xt, Xv
        self.to_device("cpu")
        torch.cuda.empty_cache()
        return {"best_epoch": self.best_epoch, **hist}

    @torch.no_grad()
    def _predict_tensor(self, Xt) -> np.ndarray:
        self.net.eval()
        bs = self.predict_batch
        return np.concatenate([torch.sigmoid(self.net(Xt[i:i + bs])).float().cpu().numpy() for i in range(0, len(Xt), bs)])

    def predict_proba(self, X):
        return self._predict_tensor(self.to_tensor(X, self.device))

    def set_threads(self, n):
        self.threads = n
        torch.set_num_threads(max(n, 1))

    def to_device(self, dev):
        self.device = dev
        self.net.to(dev)

    def n_parameters(self):
        return int(sum(p.numel() for p in self.net.parameters()))

    def _extra_meta(self):
        return {"best_epoch": getattr(self, "best_epoch", None), **self.meta()}

    def _save(self, path: Path):
        torch.save(self.net.state_dict(), path / "model.pt")

    @classmethod
    def _load(cls, path, meta):
        m = cls(meta["params"], meta["seed"])
        m.restore_meta(meta)
        m.net = m.build_net(None)
        m.net.load_state_dict(torch.load(path / "model.pt", map_location="cpu"))
        return m

    @abstractmethod
    def restore_meta(self, meta: dict) -> None: ...
