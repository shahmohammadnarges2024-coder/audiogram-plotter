# audiogram_figures_interactive.py
# Purpose:
#   Interactive, publication-ready pure-tone audiograms (Variant B: lines + large O/X markers)
#   - No pedigree or composite output
#   - Asks user which subject IDs to plot, then saves each audiogram separately

from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Config (edit as needed)
# ----------------------------

FREQ_LABELS = ["250", "500", "1000", "2000", "4000", "8000"]
X = np.arange(len(FREQ_LABELS))

SUBJECTS = {
    "II-1": {
        "right": [40, 45, 50, 55, 55, 40],
        "left":  [40, 50, 50, 55, 60, 45],
    },
    "II-2": {
        "right": [40, 50, 55, 60, 60, 65],
        "left":  [45, 50, 55, 55, 60, 65],
    },
    "II-3": {
        "right": [25, 30, 45, 50, 50, 50],
        "left":  [35, 40, 55, 55, 55, 55],
    },
}

SEVERITY_BANDS = [
    ("Normal",   -10, 20),
    ("Mild",       21, 40),
    ("Moderate",   41, 70),
    ("Severe",     71, 95),
    ("Profound",   96, 120),
]

OUTDIR = Path("fig_out_final")
OUTDIR.mkdir(parents=True, exist_ok=True)

EXPORT_EXTS = ("png", "tiff", "pdf", "svg")

plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "axes.facecolor": "white",
    "grid.color": "0.75",
    "grid.linestyle": "--",
    "grid.linewidth": 0.4,
})

# ----------------------------
# Helpers
# ----------------------------

def add_severity_bands_with_right_labels(ax: plt.Axes) -> None:
    for i, (name, y0, y1) in enumerate(SEVERITY_BANDS):
        ax.axhspan(y0, y1, color=("0.92" if i % 2 == 0 else "0.97"), zorder=0)
        ax.text(len(X) + 0.12, (y0 + y1) / 2, name,
                va="center", fontsize=8, color="0.25")

def save_all(fig: plt.Figure, stub: str) -> None:
    stub_path = OUTDIR / stub
    for ext in EXPORT_EXTS:
        fig.savefig(f"{stub_path}.{ext}", bbox_inches="tight")

def plot_single_variantB(number: str, right: list[float], left: list[float],
                         stub: str) -> None:
    fig, ax = plt.subplots(figsize=(5.8, 4.8), dpi=300)
    add_severity_bands_with_right_labels(ax)

    ax.set_axisbelow(True)
    ax.grid(True, linestyle="--", linewidth=0.4)

    ax.plot(X, right, "o-", label="Right (O)",
            linewidth=1.8, markersize=9, markeredgewidth=1.6, zorder=3)
    ax.plot(X, left,  "x--", label="Left (X)",
            linewidth=1.5, markersize=10, markeredgewidth=1.8, zorder=3)

    ax.set_xticks(X)
    ax.set_xticklabels(FREQ_LABELS)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Hearing Level (dB HL)")

    ax.set_ylim(120, -10)
    ax.set_xlim(-0.2, len(X) - 0.2)

    ax.legend(loc="upper left", frameon=True)
    ax.set_title(number, weight="bold")

    fig.tight_layout()
    save_all(fig, stub)
    plt.close(fig)

def normalize_ids(user_text: str) -> list[str]:
    # Accept: "II-1", "II-1,II-2", "II-1 II-2", "ii-1 , ii-2"
    cleaned = user_text.strip()
    if not cleaned:
        return []
    parts = cleaned.replace(",", " ").split()
    return [p.strip().upper() for p in parts if p.strip()]

# ----------------------------
# Interactive main
# ----------------------------
if __name__ == "__main__":
    print("Available IDs:")
    for k in SUBJECTS.keys():
        print(f"  - {k}")

    while True:
        raw = input("\nEnter IDs to plot (e.g., II-1 or II-2, II-3). Type q to quit: ").strip()
        if raw.lower() == "q":
            break

        ids = normalize_ids(raw)
        if not ids:
            print("No valid input. Try again.")
            continue

        for pid in ids:
            if pid not in SUBJECTS:
                print(f"[WARN] Unknown ID: {pid}. Skipped.")
                continue

            d = SUBJECTS[pid]
            stub = f"audiogram_{pid}_variantB"
            plot_single_variantB(pid, d["right"], d["left"], stub=stub)
            print(f"[OK] Saved: {stub} (all formats)")

    print(f"\nDone. Figures saved to: {OUTDIR.resolve()}")
