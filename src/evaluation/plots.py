"""Grafy jedného behu modelu (matplotlib, PNG). Jednotný štýl a farby pre celý projekt."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from sklearn.metrics import precision_recall_curve, roc_curve  # noqa: E402

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SPLIT_COLOR = {"train": "#2a78d6", "validation": "#eb6834", "test": "#1baf7a"}
SPLIT_SK = {"train": "train", "validation": "validácia", "test": "test"}
CLASS_COLOR = {0: "#2a78d6", 1: "#eb6834"}
SEQ = LinearSegmentedColormap.from_list("seq_blue", ["#f3f7fd", "#2a78d6", "#0d3a73"])


def _fig(w=7, h=5):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    return fig, ax


def _style(ax, title, xlabel="", ylabel="", grid="both"):
    ax.set_title(title, loc="left", color=INK, fontsize=12, pad=10)
    ax.set_xlabel(xlabel, color=INK2); ax.set_ylabel(ylabel, color=INK2)
    ax.tick_params(colors=INK2, length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    if grid:
        ax.grid(axis=grid, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def _save(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def roc(curves: dict, path, title):
    """curves: časť -> (y, skóre). Os x logaritmická – dôležitá je oblasť nízkeho FPR."""
    fig, ax = _fig()
    for split, (y, s) in curves.items():
        fpr, tpr, _ = roc_curve(y, s)
        ax.plot(np.maximum(fpr, 1e-5), tpr, color=SPLIT_COLOR[split], linewidth=2, label=SPLIT_SK[split])
    ax.set_xscale("log"); ax.set_xlim(1e-4, 1); ax.set_ylim(0, 1.01)
    _style(ax, title, "FPR (log. mierka)", "TPR (detekcia malvéru)")
    ax.legend(frameon=False, labelcolor=INK2, loc="lower right")
    _save(fig, path)


def pr(curves: dict, path, title):
    fig, ax = _fig()
    for split, (y, s) in curves.items():
        p, r, _ = precision_recall_curve(y, s)
        ax.plot(r, p, color=SPLIT_COLOR[split], linewidth=2, label=SPLIT_SK[split])
    ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.01)
    _style(ax, title, "recall", "precision")
    ax.legend(frameon=False, labelcolor=INK2, loc="lower left")
    _save(fig, path)


def score_hist(y, s, thresholds: dict, path, title):
    fig, ax = _fig()
    bins = np.linspace(0, 1, 51)
    for c, lab in [(0, "benign"), (1, "malware")]:
        ax.hist(s[y == c], bins=bins, color=CLASS_COLOR[c], alpha=0.75, label=lab, edgecolor=SURFACE, linewidth=0.5)
    names = {"fixed": "prah 0,5", "val_fpr": "prah z validácie (FPR 1 %)"}
    for (name, thr), ls in zip(thresholds.items(), ["--", ":"]):
        ax.axvline(thr, color=INK, linestyle=ls, linewidth=1.2, label=f"{names.get(name, name)} = {thr:.3f}")
    ax.set_yscale("log")
    _style(ax, title, "skóre P(malware)", "počet vzoriek (log.)", grid="y")
    ax.legend(frameon=False, labelcolor=INK2, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2)
    _save(fig, path)


def confusion(m: dict, path, title):
    M = np.array([[m["tn"], m["fp"]], [m["fn"], m["tp"]]])
    R = M / M.sum(axis=1, keepdims=True)
    fig, ax = _fig(4.8, 4.2)
    ax.imshow(R, cmap=SEQ, vmin=0, vmax=1)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{M[i, j]:,}\n{R[i, j]:.1%}".replace(",", " "), ha="center", va="center",
                    color="white" if R[i, j] > 0.55 else INK, fontsize=11)
    ax.set_xticks([0, 1], ["benign", "malware"]); ax.set_yticks([0, 1], ["benign", "malware"])
    _style(ax, title, "predikcia", "skutočnosť", grid=None)
    _save(fig, path)


def per_family(tables: dict, path, title):
    """tables: časť -> DataFrame(family, n, detected_rate)."""
    fams = None
    fig, ax = _fig(7.5, 5)
    h = 0.38
    for k, (split, t) in enumerate(tables.items()):
        t = t.set_index("family")
        if fams is None:
            fams = ["benign"] + sorted(f for f in t.index if f != "benign")
        y = np.arange(len(fams))[::-1]
        ax.barh(y + (0.5 - k) * h, t.loc[fams, "detected_rate"] * 100, height=h - 0.04,
                color=SPLIT_COLOR[split], label=SPLIT_SK[split])
    ax.set_yticks(np.arange(len(fams))[::-1], fams)
    ax.set_xlim(0, 100)
    _style(ax, title, "označené ako malware [%] (benign = falošné poplachy)", "", grid="x")
    ax.legend(frameon=False, labelcolor=INK2, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
    _save(fig, path)


def learning_curve(history: dict, path, title):
    key = "validation_auc"
    if key not in history or not history[key]:
        return False
    v = np.array(history[key])
    fig, ax = _fig()
    x = np.arange(1, len(v) + 1)
    ax.plot(x, v, color=SPLIT_COLOR["validation"], linewidth=2, label="ROC-AUC validácia")
    best = int(np.argmax(v))
    ax.scatter([x[best]], [v[best]], s=50, color=SPLIT_COLOR["validation"], edgecolor=SURFACE, linewidth=2, zorder=3)
    ax.annotate(f"najlepšia: {x[best]} ({v[best]:.4f})", (x[best], v[best]), textcoords="offset points",
                xytext=(6, -14), color=INK2, fontsize=9)
    lo = np.percentile(v, 5)
    ax.set_ylim(lo - (v.max() - lo) * 0.1, v.max() + (v.max() - lo) * 0.1 + 1e-6)
    _style(ax, title, "iterácia / epocha", "ROC-AUC")
    ax.legend(frameon=False, labelcolor=INK2, loc="lower right")
    _save(fig, path)
    return True


def hpo_history(trials: pd.DataFrame, path, title):
    t = trials[trials["state"] == "COMPLETE"]
    if t.empty:
        return
    fig, ax = _fig()
    ax.scatter(t["number"], t["value"], s=28, color=SPLIT_COLOR["validation"], edgecolor=SURFACE, linewidth=1.5,
               label="pokus", zorder=3)
    ax.plot(t["number"], t["value"].cummax(), color=INK2, linewidth=1.5, label="najlepší doteraz")
    _style(ax, title, "číslo pokusu", "ROC-AUC na validácii")
    ax.legend(frameon=False, labelcolor=INK2, loc="lower right")
    _save(fig, path)
