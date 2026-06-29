"""Viz: Senegal 5-0 Iraq — life and death of a contest at 13'.

This match has a sharp inflection: Senegal scored at 4', Iraq went down to ten
at 13', and the floodgates opened. The chart is a tall vertical timeline of
every event in the match, with the moment of the red card called out as the
hinge. Two side panels show how the post-13' phase totally dominated the stats.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from highlight_text import fig_text

from data.load import match_brief, match_events_long, team_stats
from style.house import apply_style, save_both, credit, INK, DIM, HOME, AWAY, BG, PANEL, ACCENT, BAD

MATCH_ID = 66

EVENT_SYMBOL = {
    "Goal": "●",
    "Assist": "·",
    "Yellow Card": "▪",
    "Red Card": "▮",
    "VAR Review": "◆",
}
EVENT_COLOR_NEUTRAL = {
    "Goal": INK,
    "Assist": DIM,
    "Yellow Card": "#E8C547",
    "Red Card": BAD,
    "VAR Review": "#9D4EDD",
}


def main(out_dir: str = "artifacts") -> tuple[str, str]:
    apply_style()
    b = match_brief(MATCH_ID)
    e = match_events_long(MATCH_ID)
    ts = team_stats().query("match_id == @MATCH_ID")
    home_ts = ts[ts.team_id == b["home_id"]].iloc[0]
    away_ts = ts[ts.team_id == b["away_id"]].iloc[0]

    fig = plt.figure(figsize=(13, 8.5))
    fig.patch.set_facecolor(BG)

    # ---- left: vertical timeline ----
    ax = fig.add_axes([0.06, 0.10, 0.36, 0.78])
    ax.set_facecolor(BG)
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(95, -2)  # top = 0', bottom = 90'

    # baseline (vertical)
    ax.axvline(0, color=DIM, lw=0.7)
    # minute ticks
    for m in (0, 15, 30, 45, 60, 75, 90):
        ax.axhline(m, color=PANEL, lw=0.6, zorder=0)
        ax.text(-1.35, m, f"{m}'", color=DIM, fontsize=10, ha="left", va="center")
    # HT
    ax.axhline(45, color=ACCENT, lw=1.0, ls=(0, (4, 4)), alpha=0.7)
    ax.text(1.3, 45, "HT", color=ACCENT, fontsize=10, ha="right", va="center")
    # RED CARD hinge highlight
    red = e[e.event_type == "Red Card"]
    for _, r in red.iterrows():
        ax.axhspan(r.minute - 1, r.minute + 1, color=BAD, alpha=0.10, zorder=0)
        ax.text(1.3, r.minute, f"{r.minute}'  RED · IRQ\n  ten-man Iraq",
                color=BAD, fontsize=10, ha="right", va="center", fontweight="bold")

    # plot events
    for _, r in e.iterrows():
        if r.event_type == "Assist":
            continue
        side = r.side
        x = 0.7 if side == "home" else -0.7
        sz = 220 if r.event_type == "Goal" else 110
        col = HOME if side == "home" else AWAY
        edge = INK if r.event_type == "Goal" else col
        # for red card override
        if r.event_type == "Red Card":
            col = BAD
        ax.scatter(x, r.minute, s=sz, color=col, edgecolor=edge, lw=1.2, zorder=4)
        # for goal, count cumulative
        if r.event_type == "Goal":
            ax.text(x, r.minute, "G", color=INK, fontsize=10, ha="center", va="center", zorder=5, fontweight="bold")
        elif r.event_type == "Red Card":
            ax.text(x, r.minute, "R", color=INK, fontsize=10, ha="center", va="center", zorder=5, fontweight="bold")
        elif r.event_type == "Yellow Card":
            ax.text(x, r.minute, "Y", color=INK, fontsize=8, ha="center", va="center", zorder=5, fontweight="bold")

    # column headers
    ax.text(0.7, -1, b["home"], color=HOME, fontsize=12, fontweight="bold", ha="center")
    ax.text(-0.7, -1, b["away"], color=AWAY, fontsize=12, fontweight="bold", ha="center")

    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])

    # ---- right: stats split ----
    ax2 = fig.add_axes([0.50, 0.10, 0.46, 0.78])
    ax2.set_facecolor(BG)
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 10)
    for sp in ax2.spines.values():
        sp.set_visible(False)
    ax2.set_xticks([]); ax2.set_yticks([])

    # full-match possession + shots ratio
    rows = [
        ("Possession", home_ts.possession_pct, away_ts.possession_pct, "%"),
        ("Total shots", home_ts.total_shots, away_ts.total_shots, ""),
        ("Shots on target", home_ts.shots_on_target, away_ts.shots_on_target, ""),
        ("Corners", home_ts.corners, away_ts.corners, ""),
        ("Saves", home_ts.saves, away_ts.saves, ""),
        ("Fouls", home_ts.fouls, away_ts.fouls, ""),
    ]
    for i, (label, hv, av, suffix) in enumerate(rows):
        y = 9 - i * 1.4
        total = hv + av
        if total == 0:
            continue
        hp = 100 * hv / total
        # bar
        ax2.barh(y, hp, color=HOME, height=0.55, alpha=0.85)
        ax2.barh(y, 100 - hp, left=hp, color=AWAY, height=0.55, alpha=0.85)
        # labels left/right
        ax2.text(-1, y, f"{hv}{suffix}", color=HOME, fontsize=11,
                 fontweight="bold", ha="right", va="center")
        ax2.text(101, y, f"{av}{suffix}", color=AWAY, fontsize=11,
                 fontweight="bold", ha="left", va="center")
        ax2.text(50, y + 0.55, label, color=DIM, fontsize=10, ha="center", va="bottom")

    ax2.set_title("90-minute match totals (Senegal · Iraq)", color=INK, fontsize=12, pad=24)

    # title block (overall)
    fig.text(0.06, 0.95, "The thirteenth minute", color=INK, fontsize=24, fontweight="bold")
    fig_text(0.06, 0.91,
             f"<{b['home']}> 5–0 <{b['away']}> · {b['date']} · {b['stadium']}",
             color=DIM, fontsize=13,
             highlight_textprops=[{"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}], fig=fig)

    fig_text(0.06, 0.06,
             "Senegal led after four minutes. Iraq's <13' red card> turned a tight start into a 5–0 demolition: "
             f"four more goals over the remaining hour and a possession-share of <{int(home_ts.possession_pct)}%–{int(away_ts.possession_pct)}%>.",
             color=INK, fontsize=11, fig=fig,
             highlight_textprops=[{"color": BAD, "fontweight": "bold"},
                                  {"color": INK, "fontweight": "bold"}])

    credit(fig)
    return save_both(fig, f"{out_dir}/senegal_iraq_redcard")


if __name__ == "__main__":
    print(main())
