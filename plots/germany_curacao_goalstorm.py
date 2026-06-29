"""Viz: Germany 7-1 Curaçao — goal-storm timeline on a pitch backdrop.

A horizontal "tempo strip" where each goal is a bubble placed at the minute it
went in, on a half-pitch backdrop (mplsoccer). Bubble size = scoreline impact
(running goal difference after the strike), color = scoring team. The story
the chart tells: Germany hit at 6', then a four-goal burst across 38'–47',
then two more after the hour — a textbook avalanche after the equaliser threat.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
from highlight_text import fig_text
from mplsoccer import VerticalPitch

from data.load import match_brief, match_events_long
from style.house import apply_style, save_both, credit, INK, DIM, HOME, AWAY, BG, PANEL, ACCENT

MATCH_ID = 9


def main(out_dir: str = "artifacts") -> tuple[str, str]:
    apply_style()
    b = match_brief(MATCH_ID)
    e = match_events_long(MATCH_ID)
    goals = e[e.event_type == "Goal"].reset_index(drop=True)

    fig = plt.figure(figsize=(13, 7.5))
    fig.patch.set_facecolor(BG)

    # left: a vertical half-pitch as a graphic anchor (no fake coordinates —
    # just the team-color "goal" panel)
    ax_pitch = fig.add_axes([0.03, 0.10, 0.28, 0.78])
    pitch = VerticalPitch(pitch_color=PANEL, line_color=DIM, half=True,
                          pad_top=2, pad_bottom=2, linewidth=1.2, goal_type="box")
    pitch.draw(ax=ax_pitch)
    ax_pitch.set_title(f"{b['home']} attacked  →", color=INK, fontsize=12, pad=10, loc="left")
    # giant scoreline overlay on the pitch
    ax_pitch.text(40, 60, f"{b['home_score']}–{b['away_score']}",
                  ha="center", va="center", color=INK, fontsize=72, fontweight="bold",
                  zorder=5)
    ax_pitch.text(40, 50, f"xG {b['home_xg']:.2f} – {b['away_xg']:.2f}",
                  ha="center", va="center", color=DIM, fontsize=12, zorder=5)

    # right: tempo strip
    ax = fig.add_axes([0.36, 0.18, 0.60, 0.55])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 95)
    ax.set_ylim(-1.2, 1.2)
    # baseline
    ax.axhline(0, color=DIM, lw=0.6, alpha=0.7)
    # minute markers
    for x in (15, 30, 45, 60, 75, 90):
        ax.axvline(x, color=PANEL, lw=0.8, zorder=0)
        ax.text(x, -1.15, f"{x}'", color=DIM, fontsize=9, ha="center", va="top")
    ax.axvspan(45, 46.5, color=ACCENT, alpha=0.10, zorder=0)
    ax.text(45.7, 1.05, "HT", color=ACCENT, fontsize=9, ha="left", va="top")

    # running diff at each goal
    h, a = 0, 0
    for _, r in goals.iterrows():
        if r.side == "home":
            h += 1
        else:
            a += 1
        diff = h - a
        y = 0.55 if r.side == "home" else -0.55
        color = HOME if r.side == "home" else AWAY
        size = 220 + abs(diff) * 140
        ax.scatter(r.minute, y, s=size, color=color, edgecolor=INK, lw=1.2, zorder=4)
        ax.text(r.minute, y, str(h if r.side == "home" else a),
                ha="center", va="center", color=INK, fontsize=10, fontweight="bold", zorder=5)
        ax.text(r.minute, y + (0.35 if r.side == "home" else -0.35),
                f"{r.minute}'", ha="center",
                va="bottom" if r.side == "home" else "top",
                color=DIM, fontsize=9, zorder=5)

    ax.text(-2, 0.85, b["home"], color=HOME, fontsize=12, fontweight="bold", ha="right", va="center")
    ax.text(-2, -0.85, b["away"], color=AWAY, fontsize=12, fontweight="bold", ha="right", va="center")

    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])

    # title block
    fig.text(0.36, 0.93, "The goal storm", color=INK, fontsize=24, fontweight="bold",
             ha="left", va="top")
    fig_text(0.36, 0.87,
             f"<{b['home']}> 7–1 <{b['away']}> · {b['date']} · {b['stadium']}",
             color=DIM, fontsize=13, ha="left", va="top",
             highlight_textprops=[{"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}], fig=fig)
    fig.text(0.36, 0.83,
             "Bubble = a goal at that minute. Number = running tally for the scoring side.",
             color=DIM, fontsize=10.5, ha="left", va="top")
    fig.text(0.36, 0.10,
             "Curaçao's lone equaliser at 21' was the only crack in a one-way game:\n"
             "four German goals in nine minutes either side of half-time turned a contest into a procession.",
             color=INK, fontsize=11, ha="left", va="top")

    credit(fig)
    base = f"{out_dir}/germany_curacao_goalstorm"
    return save_both(fig, base)


if __name__ == "__main__":
    png, svg = main()
    print(png, svg)
