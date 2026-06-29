"""Viz: France 3-1 Senegal — the last quarter-hour race.

The match's first 65 minutes produced nothing. Then four goals fell in 24
minutes. This chart overlays a cumulative-goals step plot with each team's
published-xG total as a horizontal "expected" line, then makes the 66'–90'
window a highlighted strip so the late drama is impossible to miss.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from highlight_text import fig_text

from data.load import match_brief, match_events_long
from transforms.match import running_score
from style.house import apply_style, save_both, credit, INK, DIM, HOME, AWAY, BG, PANEL, ACCENT

MATCH_ID = 17


def main(out_dir: str = "artifacts") -> tuple[str, str]:
    apply_style()
    b = match_brief(MATCH_ID)
    e = match_events_long(MATCH_ID)
    rs = running_score(MATCH_ID)

    fig = plt.figure(figsize=(13, 7.3))
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0.08, 0.18, 0.84, 0.58])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 95)
    ax.set_ylim(0, max(b["home_xg"], b["away_xg"], rs.home.max(), rs.away.max()) + 0.6)

    # highlighted late window
    ax.axvspan(66, 95, color=ACCENT, alpha=0.07, zorder=0)

    # gridlines + minute labels
    for x in (15, 30, 45, 60, 75, 90):
        ax.axvline(x, color=PANEL, lw=0.6, zorder=0)
    ax.axvline(45, color=DIM, ls=(0, (4, 4)), lw=0.7, zorder=0)
    ax.text(45.5, ax.get_ylim()[1] - 0.05, "HT", color=DIM, fontsize=9, va="top")

    # xG horizontal "expected" lines
    ax.axhline(b["home_xg"], color=HOME, lw=1.3, ls=(0, (5, 4)), alpha=0.7)
    ax.axhline(b["away_xg"], color=AWAY, lw=1.3, ls=(0, (5, 4)), alpha=0.7)
    ax.text(0.5, b["home_xg"], f" xG = {b['home_xg']:.2f}", color=HOME, fontsize=10,
            va="center", ha="left", backgroundcolor=BG)
    ax.text(0.5, b["away_xg"], f" xG = {b['away_xg']:.2f}", color=AWAY, fontsize=10,
            va="center", ha="left", backgroundcolor=BG)

    # actual goals as step series
    ax.step(rs.minute, rs.home, where="post", color=HOME, lw=3)
    ax.step(rs.minute, rs.away, where="post", color=AWAY, lw=3)

    # bubbles at each goal minute
    goals = e[e.event_type == "Goal"]
    h, a = 0, 0
    for _, g in goals.iterrows():
        if g.side == "home":
            h += 1
            y = h
            col = HOME
        else:
            a += 1
            y = a
            col = AWAY
        ax.scatter(g.minute, y, s=140, color=col, edgecolor=INK, lw=1.4, zorder=5)
        ax.text(g.minute, y + 0.18, f"{g.minute}'", color=col, fontsize=10,
                ha="center", va="bottom", fontweight="bold")

    # axes cosmetics
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_xticklabels([f"{x}'" for x in [0, 15, 30, 45, 60, 75, 90]])
    ax.tick_params(colors=DIM)
    ax.set_ylabel("Cumulative", color=DIM, fontsize=10)
    ax.grid(axis="y", color=PANEL, lw=0.6)

    # final-score labels at right
    ax.text(93, rs.home.iloc[-1], f"  {int(rs.home.iloc[-1])}", color=HOME, fontsize=22,
            fontweight="bold", va="center")
    ax.text(93, rs.away.iloc[-1], f"  {int(rs.away.iloc[-1])}", color=AWAY, fontsize=22,
            fontweight="bold", va="center")
    ax.text(80, ax.get_ylim()[1] - 0.18, "the 24-minute storm",
            color=ACCENT, fontsize=10, fontweight="bold", ha="center")

    # title block
    fig.text(0.08, 0.93, "The race that started in the 66th", color=INK, fontsize=22, fontweight="bold")
    fig_text(0.08, 0.87,
             f"<{b['home']}> 3–1 <{b['away']}> · {b['date']} · {b['stadium']}",
             color=DIM, fontsize=13,
             highlight_textprops=[{"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}], fig=fig)
    fig.text(0.08, 0.83,
             "Solid steps = actual cumulative goals. Dashed lines = each team's published xG total.",
             color=DIM, fontsize=10.5)

    fig_text(0.08, 0.08,
             "Nothing for 65 minutes, then a deluge: <France>'s 66' opener triggered a four-goal flurry "
             "across the final 24 minutes, finishing 0.56 xG above their expected total. "
             "<Senegal>'s 90' consolation kept them within 0.05 of theirs.",
             color=INK, fontsize=11, fig=fig,
             highlight_textprops=[{"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}])

    credit(fig)
    return save_both(fig, f"{out_dir}/france_senegal_xg_race")


if __name__ == "__main__":
    print(main())
