"""Viz: Netherlands 5-1 Sweden — efficiency vs volume (mplsoccer PyPizza).

Sweden out-shot the Dutch 16 to 10 and led on shots-on-target (8 to 7) and
possession was nearly level (48–43%). The chart uses mplsoccer's PyPizza to
slice the match into team shares of each stat: a striking visual of Sweden
owning the *volume* stats while Netherlands owned the only one that matters.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import numpy as np

from data.load import match_brief, team_stats
from style.house import apply_style, save_both, credit, INK, DIM, HOME, AWAY, BG, PANEL, ACCENT, GOOD, BAD

MATCH_ID = 35

METRICS = [
    ("Possession", "possession_pct"),
    ("Total shots", "total_shots"),
    ("Shots on target", "shots_on_target"),
    ("Corners", "corners"),
    ("Saves", "saves"),
]


def main(out_dir: str = "artifacts") -> tuple[str, str]:
    apply_style()
    b = match_brief(MATCH_ID)
    ts = team_stats().query("match_id == @MATCH_ID")
    h = ts[ts.team_id == b["home_id"]].iloc[0]
    a = ts[ts.team_id == b["away_id"]].iloc[0]

    # Share of each metric (home as %, with the score itself appended so we keep
    # the "goal" stat in the radar at full value).
    labels = [m[0] for m in METRICS] + ["Goals"]
    home_share, away_share, raw_h, raw_a = [], [], [], []
    for _, col in METRICS:
        hv = float(h[col]); av = float(a[col])
        tot = hv + av if (hv + av) > 0 else 1
        home_share.append(100 * hv / tot)
        away_share.append(100 * av / tot)
        raw_h.append(hv); raw_a.append(av)
    # Goals
    hg, ag = b["home_score"], b["away_score"]
    tot = hg + ag if (hg + ag) > 0 else 1
    home_share.append(100 * hg / tot)
    away_share.append(100 * ag / tot)
    raw_h.append(hg); raw_a.append(ag)

    # Build two pizzas side-by-side
    fig = plt.figure(figsize=(13, 8.6))
    fig.patch.set_facecolor(BG)

    for i, (share, raw, name, color, x0) in enumerate([
        (home_share, raw_h, b["home"], HOME, 0.04),
        (away_share, raw_a, b["away"], AWAY, 0.52),
    ]):
        ax = fig.add_axes([x0, 0.10, 0.44, 0.66], projection="polar")
        ax.set_facecolor(BG)
        pizza = PyPizza(
            params=labels,
            background_color=BG,
            straight_line_color=PANEL,
            straight_line_lw=1,
            last_circle_lw=0,
            other_circle_lw=0,
            inner_circle_size=8,
        )
        pizza.make_pizza(
            share,
            ax=ax,
            color_blank_space="same",
            blank_alpha=0.04,
            kwargs_slices=dict(facecolor=color, edgecolor=BG, alpha=0.85, zorder=2),
            kwargs_params=dict(color=DIM, fontsize=10, va="center"),
            kwargs_values=dict(
                color=INK, fontsize=11, fontweight="bold",
                bbox=dict(edgecolor=color, facecolor=color, boxstyle="round,pad=0.18", lw=1)
            ),
        )
        # custom values: show raw count, not the share %
        # PyPizza renders share text by default; override by setting texts after the call
        for t, val_raw in zip(ax.texts[len(labels):], raw):
            if val_raw == int(val_raw):
                t.set_text(str(int(val_raw)))
            else:
                t.set_text(f"{val_raw:.0f}")
        ax.set_title(name, color=color, fontsize=18, fontweight="bold", pad=22)

    # title block
    fig.text(0.04, 0.95, "Volume vs payout",
             color=INK, fontsize=24, fontweight="bold")
    fig.text(0.04, 0.91,
             f"{b['home']} 5–1 {b['away']} · {b['date']} · {b['stadium']}",
             color=DIM, fontsize=13)
    fig.text(0.04, 0.875,
             "Each slice shows that team's share of the match total; numbers are the team's raw count.",
             color=DIM, fontsize=10.5)

    fig.text(0.04, 0.04,
             f"Sweden took more shots (16 vs 10), more shots on target (8 vs 7) and made more saves (7 vs 2) — "
             "but only one of their efforts went in. Netherlands turned a thinner deck into five goals.",
             color=INK, fontsize=11)

    credit(fig)
    return save_both(fig, f"{out_dir}/netherlands_sweden_pizza")


if __name__ == "__main__":
    print(main())
