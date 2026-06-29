"""House style: dark editorial look with a hint of warm accent.

Palette intent: a near-black newsprint feel, off-white type, gold accent for
emphasis, two contrasting team colors (cool/warm) that read as opposing sides.
Colorblind-aware: blue vs amber, never red vs green alone.
"""
from __future__ import annotations
import matplotlib as mpl
import matplotlib.pyplot as plt

# --- palette -------------------------------------------------------------
BG = "#0E1116"          # background (near-black, slight blue)
PANEL = "#161A22"       # secondary panel
INK = "#ECECEC"         # primary text
DIM = "#9AA0A6"         # secondary text
GRID = "#262A33"        # gridline
ACCENT = "#E8C547"      # gold accent
HOME = "#3DA5D9"        # team A — cool blue
AWAY = "#F18F01"        # team B — warm amber
NEUTRAL = "#7C8794"
GOOD = "#7FB069"
BAD = "#D7263D"

# Confederation palette (used for cross-tournament views, optional here)
CONF = {
    "UEFA":     "#3DA5D9",
    "CONMEBOL": "#F4D35E",
    "CONCACAF": "#EE6055",
    "CAF":      "#73AB84",
    "AFC":      "#9D4EDD",
    "OFC":      "#06A77D",
}


def apply_style() -> None:
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "xtick.color": DIM,
        "ytick.color": DIM,
        "text.color": INK,
        "grid.color": GRID,
        "grid.alpha": 0.6,
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": False,
        "font.family": ["DejaVu Sans"],
        "font.size": 11,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
    })


def credit(fig, text: str = "data · Kaggle mominullptr/fifa-world-cup-2026 · viz · boxwheel/wc2026-viz-match-stories") -> None:
    fig.text(0.01, 0.005, text, fontsize=7.5, color=DIM, ha="left", va="bottom")


def title_block(fig, title: str, subtitle: str, x: float = 0.04, y: float = 0.96) -> None:
    fig.text(x, y, title, fontsize=20, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(x, y - 0.045, subtitle, fontsize=12, color=DIM, ha="left", va="top")


def save_both(fig, path_no_ext: str) -> tuple[str, str]:
    """Save fig as PNG@200dpi and SVG. Returns (png_path, svg_path)."""
    png = f"{path_no_ext}.png"
    svg = f"{path_no_ext}.svg"
    fig.savefig(png, dpi=200)
    fig.savefig(svg)
    return png, svg
