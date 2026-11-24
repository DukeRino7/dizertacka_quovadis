"""Grafy pre docs/21 (porovnanie datasetov Quo Vadis a KronoDroid).

Čísla sú prevzaté z výstupov skriptov (nie odhadnuté):
- Quo Vadis: docs/07 (časový test, prah z validácie), docs/10 (zero-day, prah z validácie, oddiely 2 a 6.1).
- KronoDroid: runs_v4/comparison/v4/README.md (O1, O2, D-norm s IS) a výpočet z uložených predikcií tým istým
  kódom (src.evaluation.v4_report: Setting, main_metrics, zero_day_metrics), prah z validácie.
Spustenie: .venv\\Scripts\\python.exe docs\\21_zdroj\\make_figures.py  → SVG v docs/21_zdroj/
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).parent
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#ffffff"
C = {"stat": "#2a78d6", "dyn": "#eb6834", "hyb": "#1baf7a"}   # pevné poradie farieb (statický, dynamický, hybrid)
NAME = {"stat": "statický", "dyn": "dynamický", "hyb": "hybridný"}

plt.rcParams.update({
    "font.family": ["Segoe UI", "Calibri", "Arial", "DejaVu Sans"], "font.size": 9, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": GRID, "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURF,
    "figure.facecolor": SURF, "svg.fonttype": "none", "axes.spines.top": False, "axes.spines.right": False,
})


from matplotlib.ticker import FuncFormatter  # noqa: E402

COMMA = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",").replace("-", "−"))


def _axes(ax, ylabel=None):
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    if ylabel:
        ax.set_ylabel(ylabel)


# ---------------------------------------------------------------- obr. 1: tri prístupy na dvoch datasetoch
def fig_approaches():
    data = {  # TPR pri prahu z validácie (FPR ≤ 1 % na validácii)
        "známe rodiny": {"Quo Vadis\n(časový test)": (0.9843, 0.6572, 0.9842),
                         "KronoDroid\n(náhodný test)": (0.9459, 0.8688, 0.9724)},
        "nové rodiny (zero-day)": {"Quo Vadis\n(7 rodín)": (0.792, 0.509, 0.787),
                                   "KronoDroid\n(5 rodín)": (0.678, 0.635, 0.836)},
    }
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    w = 0.26
    for ax, (title, groups) in zip(axes, data.items()):
        for gi, (g, vals) in enumerate(groups.items()):
            for j, k in enumerate(("stat", "dyn", "hyb")):
                x = gi + (j - 1) * (w + 0.02)
                ax.bar(x, vals[j], w, color=C[k], edgecolor=SURF, linewidth=1, label=NAME[k] if gi == 0 else None)
                ax.text(x, vals[j] + 0.015, f"{vals[j]:.2f}".replace(".", ","), ha="center", va="bottom",
                        fontsize=7.5, color=INK)
        ax.set_xticks(range(len(groups)), list(groups))
        ax.set_title(title, fontsize=9.5, color=INK, loc="left")
        ax.set_ylim(0, 1.08)
        _axes(ax, "podiel zachyteného malvéru (TPR)" if ax is axes[0] else None)
        ax.yaxis.set_major_formatter(COMMA)
    axes[0].legend(loc="lower left", frameon=False, ncol=3, bbox_to_anchor=(0, -0.38))
    fig.tight_layout()
    fig.savefig(OUT / "obr1_pristupy.svg")


# ---------------------------------------------------------------- obr. 2: rozdiely s intervalmi spoľahlivosti
def fig_forest():
    rows = [  # (popis, bod, dolná, horná, kritérium splnené?)  – p. b., TPR pri FPR 1 % (ROC testu)
        ("O1: hybrid − statický, známe rodiny", 1.78, 1.15, 2.38, True),
        ("O1-Z: hybrid − statický, nové rodiny", 11.38, 9.70, 13.00, True),
        ("D-norm: to isté s podielmi volaní", 1.74, 1.14, 2.36, True),
        ("zariadenie: hybrid − statický", 2.76, 2.01, 3.46, None),
        ("emulátor: hybrid − statický", 2.00, 1.32, 2.63, None),
        ("O2: zariadenie − emulátor, známe rodiny", 0.76, 0.30, 1.28, False),
        ("O2-Z: zariadenie − emulátor, nové rodiny", 9.60, 8.33, 10.82, True),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    for i, (lab, p, lo, hi, ok) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.plot([lo, hi], [y, y], color=INK2, linewidth=2, solid_capstyle="round")
        face = MUTED if ok is None else (C["stat"] if ok else SURF)   # sivá = popisný údaj, nie kritérium
        edge = MUTED if ok is None else C["stat"]
        ax.plot(p, y, "o", markersize=8, markerfacecolor=face, markeredgecolor=edge, markeredgewidth=2)
        txt = f"{p:+.2f}".replace(".", ",")
        ax.text(hi + 0.3, y, txt, va="center", fontsize=8, color=INK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1])
    ax.axvline(0, color=INK2, linewidth=1)
    ax.axvline(1, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    ax.text(1.1, len(rows) - 0.45, "hranica kritéria +1 p. b.", fontsize=7.5, color=MUTED)
    ax.set_xlim(-0.5, 14.5)
    ax.set_xlabel("rozdiel (p. b.) s 95 % intervalom spoľahlivosti")
    ax.xaxis.set_major_formatter(COMMA)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    ax.spines["left"].set_visible(False)
    ax.set_ylim(-0.6, len(rows) - 0.2)
    fig.tight_layout()
    fig.savefig(OUT / "obr2_rozdiely.svg")


# ---------------------------------------------------------------- obr. 3: po rodinách, statický vs. hybrid
def fig_families():
    qv = {  # Quo Vadis, docs/10 oddiel 2 (prah z validácie)
        "backdoor": (0.984, 0.986), "coinminer": (0.601, 0.597), "dropper": (0.943, 0.947),
        "keylogger": (0.241, 0.168), "ransomware": (0.982, 0.985), "rat": (0.923, 0.947), "trojan": (0.872, 0.879)}
    kd = {  # KronoDroid real_full (prah z validácie)
        "Airpush/StopSMS": (0.500, 0.880), "Boxer": (0.740, 0.942), "FakeInst": (0.823, 0.923),
        "Locker/SLocker": (0.343, 0.439), "BankBot": (0.985, 0.994)}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), sharex=True,
                             gridspec_kw={"width_ratios": [1, 1]})
    for ax, (title, d) in zip(axes, (("Quo Vadis\n(Windows, emulácia Speakeasy)", qv),
                                     ("KronoDroid\n(Android, skutočné zariadenie)", kd))):
        fams = list(d)[::-1]
        for y, f in enumerate(fams):
            s, h = d[f]
            ax.plot([s, h], [y, y], color=GRID, linewidth=3, solid_capstyle="round", zorder=1)
            ax.plot(s, y, "o", ms=8, color=C["stat"], mec=SURF, mew=2, zorder=3)
            ax.plot(h, y, "o", ms=8, color=C["hyb"], mec=SURF, mew=2, zorder=3)
            dd = round((h - s) * 100)
            ax.text(1.06, y, "0" if dd == 0 else f"{dd:+d}".replace("-", "−"), va="center", fontsize=8,
                    color=INK if abs(dd) >= 1 else MUTED, transform=ax.get_yaxis_transform())
        ax.set_yticks(range(len(fams)), fams)
        ax.set_xlim(0, 1.02)
        ax.set_title(title, fontsize=9, loc="left")
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(length=0)
        ax.spines["left"].set_visible(False)
        ax.set_xlabel("TPR vynechanej rodiny")
    for ax in axes:
        ax.xaxis.set_major_formatter(COMMA)
    h1 = plt.Line2D([], [], marker="o", ls="", ms=8, color=C["stat"], label="statický")
    h2 = plt.Line2D([], [], marker="o", ls="", ms=8, color=C["hyb"], label="hybridný")
    fig.legend(handles=[h1, h2], loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.06, 0.97, 1), w_pad=3)
    fig.savefig(OUT / "obr3_rodiny.svg")


# ---------------------------------------------------------------- obr. 4: zariadenie vs. emulátor po rodinách
def fig_device():
    fams = ["Airpush/StopSMS", "Boxer", "FakeInst", "Locker/SLocker", "BankBot"]
    dyn = {"zariadenie": (0.840, 0.513, 0.564, 0.495, 0.755), "emulátor": (0.552, 0.349, 0.354, 0.198, 0.854)}
    hyb = {"zariadenie": (0.873, 0.940, 0.945, 0.531, 0.993), "emulátor": (0.617, 0.928, 0.895, 0.391, 0.991)}
    stat = (0.479, 0.905, 0.829, 0.358, 0.984)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=True)
    for ax, (title, d, col) in zip(axes, (("dynamický model", dyn, C["dyn"]), ("hybridný model", hyb, C["hyb"]))):
        for i, f in enumerate(fams[::-1]):
            k = len(fams) - 1 - i
            e, r = d["emulátor"][k], d["zariadenie"][k]
            ax.plot([e, r], [i, i], color=GRID, linewidth=3, solid_capstyle="round", zorder=1)
            ax.plot(e, i, "o", ms=8, mfc=SURF, mec=col, mew=2, zorder=3)
            ax.plot(r, i, "o", ms=8, color=col, mec=SURF, mew=1.5, zorder=3)
            ax.plot(stat[k], i, "|", ms=11, mew=2, color=C["stat"], zorder=2)
        ax.set_yticks(range(len(fams)), fams[::-1])
        ax.set_xlim(0, 1.02)
        ax.set_title(title, fontsize=9.5, loc="left")
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(length=0)
        ax.spines["left"].set_visible(False)
        ax.set_xlabel("TPR vynechanej rodiny")
        ax.xaxis.set_major_formatter(COMMA)
    hs = [plt.Line2D([], [], marker="o", ls="", ms=8, color=INK2, label="dynamika zo zariadenia"),
          plt.Line2D([], [], marker="o", ls="", ms=8, mfc=SURF, mec=INK2, mew=2, label="dynamika z emulátora"),
          plt.Line2D([], [], marker="|", ls="", ms=11, mew=2, color=C["stat"], label="statický model (rovnaký)")]
    fig.legend(handles=hs, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(OUT / "obr4_zariadenie_emulator.svg")


if __name__ == "__main__":
    fig_approaches()
    fig_forest()
    fig_families()
    fig_device()
    print("hotovo:", sorted(p.name for p in OUT.glob("*.svg")))
