# audiogram_tool_input_thresholds.py
# Interactive audiogram plotter: asks for ID + thresholds, then saves each figure.

from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

FREQ_LABELS = ["250", "500", "1000", "2000", "4000", "8000"]
X = np.arange(len(FREQ_LABELS))

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

def add_severity_bands_with_right_labels(ax: plt.Axes) -> None:
    for i, (name, y0, y1) in enumerate(SEVERITY_BANDS):
        ax.axhspan(y0, y1, color=("0.92" if i % 2 == 0 else "0.97"), zorder=0)
        ax.text(len(X) + 0.12, (y0 + y1) / 2, name,
                va="center", fontsize=8, color="0.25")

def save_all(fig: plt.Figure, stub: str) -> None:
    base = OUTDIR / stub
    for ext in EXPORT_EXTS:
        fig.savefig(f"{base}.{ext}", bbox_inches="tight")

def parse_six_numbers(prompt: str) -> list[float]:
    """
    Ask user for exactly 6 numbers (250..8000 Hz).
    Accepts: space or comma separated.
    """
    while True:
        raw = input(prompt).strip()
        parts = raw.replace(",", " ").split()
        if len(parts) != 6:
            print("⚠️ دقیقا 6 عدد وارد کن (برای 250 تا 8000). مثال: 40 45 50 55 55 40")
            continue
        try:
            vals = [float(p) for p in parts]
        except ValueError:
            print("⚠️ فقط عدد وارد کن. مثال: 40 45 50 55 55 40")
            continue
        return vals

def plot_single_variantB(subject_id: str, right: list[float], left: list[float]) -> None:
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
    ax.set_title(subject_id, weight="bold")

    fig.tight_layout()

    safe_id = subject_id.replace(" ", "_").replace("/", "-").replace("\\", "-")
    save_all(fig, f"audiogram_{safe_id}_variantB")
    plt.close(fig)

if __name__ == "__main__":
    print("Interactive Audiogram Tool (type q to quit)")
    print("Order is always: 250 500 1000 2000 4000 8000 (dB HL)")

    while True:
        sid = input("\nEnter subject ID (e.g., II-1). Type q to quit: ").strip()
        if sid.lower() == "q":
            break
        if not sid:
            print("⚠️ یک ID وارد کن.")
            continue

        right = parse_six_numbers("Right ear thresholds (6 numbers): ")
        left  = parse_six_numbers("Left  ear thresholds (6 numbers): ")

        plot_single_variantB(sid, right, left)
        print(f"[OK] Saved: audiogram_{sid}_variantB (all formats)")

    print(f"\nDone. Figures saved to: {OUTDIR.resolve()}")
