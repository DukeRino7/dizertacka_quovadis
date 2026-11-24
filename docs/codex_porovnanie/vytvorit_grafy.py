"""Vytvorí tri vektorové grafy pre porovnanie; pracuje len s uloženými súhrnmi."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUTPUT = Path(__file__).resolve().parent
ROOT = OUTPUT.parents[1]
NAVY = "#163c52"
TEAL = "#007d77"
ORANGE = "#9b551b"
GREY = "#516779"
LIGHT = "#d7e1e7"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10.5,
    "text.color": NAVY, "axes.labelcolor": NAVY, "xtick.color": GREY, "ytick.color": NAVY,
    "svg.fonttype": "path", "svg.hashsalt": "porovnanie-datasetov",
})


def sk_number(value, *, sign=False):
    return format(value, "+.2f" if sign else ".2f").replace("-", "−").replace(".", ",")


def axes(height, left, xlim, ticks, labels):
    fig, ax = plt.subplots(figsize=(7.25, height))
    fig.subplots_adjust(left=left, right=.975, bottom=.25 if height < 2.75 else .22, top=.92)
    ax.set_xlim(*xlim)
    ax.set_xticks(ticks)
    ax.set_ylim(len(labels) - .5, -.55)
    ax.set_yticks(range(len(labels)), labels)
    ax.tick_params(axis="both", length=0, pad=5)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: str(int(x)).replace("-", "−")))
    ax.grid(axis="x", color=LIGHT, linewidth=.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig, ax


def save(fig, name):
    fig.savefig(OUTPUT / f"graf_{name}.svg", metadata={"Date": None})
    plt.close(fig)


def interval(ax, y, point, lower, upper, color):
    errors = None if lower is None else [[point - lower], [upper - point]]
    ax.errorbar(point, y, xerr=errors, fmt="o", color=color, elinewidth=2.2,
                capsize=3.4, markersize=6, zorder=4)
    ax.annotate(sk_number(point, sign=True), (upper if errors else point, y),
                xytext=(7, 0), textcoords="offset points", va="center",
                fontweight="bold", color=color)


def draw_questions(criteria):
    names = ("O1", "O1-Z", "O2", "O2-Z")
    fig, ax = axes(2.35, .245, (-.35, 15.8), (0, 2, 4, 6, 8, 10, 12, 14),
                   ("O1 · hlavný test", "O1-Z · nová rodina",
                    "O2 · hlavný test", "O2-Z · nová rodina"))
    ax.axvline(0, color=GREY, linewidth=.85)
    ax.axvline(1, color=ORANGE, linewidth=1.05, linestyle=(0, (3, 3)))
    for y, name in enumerate(names):
        row = criteria[name]
        interval(ax, y, *(row[key] * 100 for key in ("point", "lo", "hi")),
                 TEAL if row["met"] else ORANGE)
    ax.set_xlabel("Rozdiel citlivosti (p. b.)")
    save(fig, "otazky")


def draw_families(rows):
    def by_family(branch):
        return {r["rodina"]: r for r in rows
                if r["vetva"] == branch and r["n"] is not None and r["rodina"] != "priemer"}

    real, emu = by_family("real_p"), by_family("emu_p")
    names = ["Airpush/StopSMS", "Boxer", "FakeInst", "Locker/SLocker Ransomware", "BankBot"]
    def display_name(n):
        return "Locker/SLocker" if n.startswith("Locker/") else n

    labels = [f"{display_name(n)} ({real[n]['n']:,})".replace(",", " ") for n in names]
    fig, ax = axes(2.70, .29, (33, 103), tuple(range(40, 101, 10)), labels)
    fig.subplots_adjust(bottom=.32)
    for y, family in enumerate(names):
        r, e = real[family], emu[family]
        assert r["n"] == e["n"] and r["statický (vybraný)"] == e["statický (vybraný)"]
        static = r["statický (vybraný)"] * 100
        device = r["hybrid (vybraný)"] * 100
        emulator = e["hybrid (vybraný)"] * 100
        ax.plot([emulator, device], [y + .07, y - .07], color="#9cb8bf", linewidth=2.0)
        for value, marker, color, desc, order in (
            (static, "|", GREY, "Spoločná statika", 2),
            (emulator, "D", ORANGE, "Hybrid · emulátor", 3),
            (device, "o", TEAL, "Hybrid · zariadenie", 4),
        ):
            offset = .16 if marker == "|" else (.07 if marker == "D" else -.07)
            ax.plot(value, y + offset, marker=marker, color=color, markersize=9 if marker == "|" else 5.5,
                    linestyle="none", markeredgewidth=1.6, label=desc if y == 0 else None, zorder=order)
    ax.set_xlabel("TPR (%)")
    fig.legend(loc="lower center", bbox_to_anchor=(.53, .065), frameon=False,
              ncol=3, fontsize=8.7, columnspacing=1.35, handletextpad=.4)
    save(fig, "rodiny")


def draw_comparison(derived, criteria, time_rows):
    def difference(key, *, zero=False):
        row = derived[key]["mean"] if zero else derived[key]
        return 100 * (row["hybrid"] - row["static"])

    def span(name):
        return tuple(criteria[name][key] * 100 for key in ("point", "lo", "hi"))

    # Súhrn V4 uvádza interval pre doplnkový časový scenár.
    time_point = 100 * (time_rows[2]["TPR pri FPR 1 % (test)"] - time_rows[0]["TPR pri FPR 1 % (test)"])
    values = [
        (difference("qv_main_roc"), None, None),
        (difference("qv_zero_test_roc", zero=True), None, None),
        (difference("qv_zero_with_holdout_roc", zero=True), None, None),
        span("O1"), span("O1-Z"), (time_point, 3.98, 7.20),
    ]
    labels = (
        "Quo Vadis · aprílový test",
        "Quo Vadis · nová rodina (apríl)",
        "Quo Vadis · nová rodina (jan. + apr.)",
        "KronoDroid · hlavný test",
        "KronoDroid · nová rodina",
        "KronoDroid · časový posun malvéru",
    )
    fig, ax = axes(2.8, .425, (-3.3, 16.5), (-2, 0, 2, 4, 6, 8, 10, 12, 14), labels)
    ax.axvline(0, color=GREY, linewidth=1.1)
    ax.axhline(2.5, color=LIGHT, linewidth=.9, zorder=1)
    for y, (point, lo, hi) in enumerate(values):
        interval(ax, y, point, lo, hi, NAVY if y < 3 else TEAL)
    ax.set_xlabel("TPR hybridu mínus TPR statického modelu (p. b.)")
    save(fig, "porovnanie")


def main():
    raw = json.loads((ROOT / "runs_v4" / "comparison" / "v4" / "summary.json").read_text(encoding="utf-8"))
    derived = json.loads((OUTPUT / "overene_hodnoty.json").read_text(encoding="utf-8"))
    criteria = {row["id"]: row for row in raw["criteria"]}
    draw_questions(criteria)
    draw_families(raw["zero_day"])
    draw_comparison(derived, criteria, raw["time"])


if __name__ == "__main__":
    main()

