"""Viz: Mexico 2-0 South Africa — the opener that emptied a team.

The tournament's opening fixture finished 10 v 9. The chart pairs a card
chronology (three rectangles dropped on a horizontal timeline, two RSA reds
followed by a Mexico red) with two stepped player-count lines that show each
team's number of players on the pitch at every minute.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from highlight_text import fig_text

from data.load import match_brief, match_events_long
from style.house import apply_style, save_both, credit, INK, DIM, HOME, AWAY, BG, PANEL, ACCENT, BAD

MATCH_ID = 1


def main(out_dir: str = "artifacts") -> tuple[str, str]:
    apply_style()
    b = match_brief(MATCH_ID)
    e = match_events_long(MATCH_ID)

    fig = plt.figure(figsize=(13, 7.4))
    fig.patch.set_facecolor(BG)

    # ---- top: player counts over time (step) ----
    ax = fig.add_axes([0.08, 0.45, 0.84, 0.36])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 95)
    ax.set_ylim(8, 11.6)

    # build per-minute counts
    minutes = list(range(0, 96))
    home_n = [11] * len(minutes)
    away_n = [11] * len(minutes)
    reds = e[e.event_type == "Red Card"].sort_values("minute")
    for _, r in reds.iterrows():
        idx = int(r.minute)
        target = home_n if r.side == "home" else away_n
        for m in range(idx, len(minutes)):
            target[m] -= 1

    ax.step(minutes, home_n, where="post", color=HOME, lw=3, label=b["home"])
    ax.step(minutes, away_n, where="post", color=AWAY, lw=3, label=b["away"])
    ax.fill_between(minutes, 11, home_n, step="post", color=HOME, alpha=0.10)
    ax.fill_between(minutes, 11, away_n, step="post", color=AWAY, alpha=0.10)

    # half-time
    ax.axvline(45, color=DIM, ls=(0, (4, 4)), lw=0.6)
    ax.text(45.6, 11.45, "HT", color=DIM, fontsize=9, va="top")

    # red card markers vertical
    for _, r in reds.iterrows():
        col = HOME if r.side == "home" else AWAY
        ax.axvline(r.minute, color=BAD, lw=1.2, alpha=0.8)
        ax.scatter(r.minute, 9 if r.side == "away" else 10, s=320, marker="s",
                   color=BAD, edgecolor=INK, lw=1.3, zorder=5)
        ax.text(r.minute, 8.5,
                f"{r.minute}'\nRED · {(b['home'] if r.side=='home' else b['away'])[:3].upper()}",
                color=BAD, fontsize=9, ha="center", va="top", fontweight="bold")

    # goal markers (different color)
    goals = e[e.event_type == "Goal"]
    for _, g in goals.iterrows():
        col = HOME if g.side == "home" else AWAY
        ax.scatter(g.minute, 11.25, s=180, color=col, edgecolor=INK, lw=1.2, zorder=5)
        ax.text(g.minute, 11.55, f"{g.minute}'", color=col, fontsize=9, ha="center",
                va="bottom", fontweight="bold")

    # axis cosmetics
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_xticklabels([f"{x}'" for x in [0, 15, 30, 45, 60, 75, 90]])
    ax.set_yticks([9, 10, 11])
    ax.set_yticklabels(["9 v", "10 v", "11 v"])
    ax.tick_params(colors=DIM)
    ax.grid(axis="y", color=PANEL, lw=0.6)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(PANEL)
    ax.set_ylabel("players on pitch", color=DIM, fontsize=10)

    # team labels at right edge
    ax.text(93, home_n[-1], f"  {home_n[-1]}", color=HOME, fontsize=18, fontweight="bold", va="center")
    ax.text(93, away_n[-1], f"  {away_n[-1]}", color=AWAY, fontsize=18, fontweight="bold", va="center")

    # ---- bottom: incident chronology as bars ----
    ax2 = fig.add_axes([0.08, 0.20, 0.84, 0.18])
    ax2.set_facecolor(BG)
    ax2.set_xlim(0, 95)
    ax2.set_ylim(-0.7, 0.7)
    ax2.axhline(0, color=DIM, lw=0.5)
    for x in (15, 30, 45, 60, 75, 90):
        ax2.text(x, -0.65, f"{x}'", color=DIM, fontsize=9, ha="center", va="top")
    # plot incidents as small rectangles
    for _, ev in e.iterrows():
        side = ev.side
        y = 0.18 if side == "home" else -0.18
        col = HOME if side == "home" else AWAY
        if ev.event_type == "Goal":
            ax2.add_patch(Rectangle((ev.minute - 0.4, y - 0.10), 0.8, 0.22,
                                    color=col, ec=INK, lw=0.6))
            ax2.text(ev.minute, y, "G", color=INK, fontsize=8, ha="center", va="center", fontweight="bold")
        elif ev.event_type == "Red Card":
            ax2.add_patch(Rectangle((ev.minute - 0.4, y - 0.18), 0.8, 0.36,
                                    color=BAD, ec=INK, lw=0.6))
            ax2.text(ev.minute, y, "R", color=INK, fontsize=8, ha="center", va="center", fontweight="bold")
        elif ev.event_type == "VAR Review":
            ax2.add_patch(Rectangle((ev.minute - 0.4, y - 0.10), 0.8, 0.22,
                                    color="#9D4EDD", ec=INK, lw=0.4))
            ax2.text(ev.minute, y, "V", color=INK, fontsize=8, ha="center", va="center", fontweight="bold")
    for sp in ax2.spines.values():
        sp.set_visible(False)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.text(-1, 0.18, b["home"], color=HOME, fontsize=10, fontweight="bold", ha="right", va="center")
    ax2.text(-1, -0.18, b["away"], color=AWAY, fontsize=10, fontweight="bold", ha="right", va="center")

    # title block
    fig.text(0.08, 0.92, "10 v 9: the opener that emptied a team", color=INK, fontsize=22, fontweight="bold")
    fig_text(0.08, 0.87,
             f"<{b['home']}> 2–0 <{b['away']}> · {b['date']} · {b['stadium']}",
             color=DIM, fontsize=13,
             highlight_textprops=[{"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}], fig=fig)
    fig.text(0.08, 0.83,
             "Top: players-on-pitch over 90'. Bottom: every event in chronological strips. Red = red card; G = goal; V = VAR.",
             color=DIM, fontsize=10.5)

    fig_text(0.08, 0.10,
             "An opening fixture finished as a player-count puzzle: <South Africa> finished with nine, <Mexico> with ten. "
             "All three reds came in the second half, after Mexico had already taken control through Quiñones' 9' opener.",
             color=INK, fontsize=11, fig=fig,
             highlight_textprops=[{"color": AWAY, "fontweight": "bold"},
                                  {"color": HOME, "fontweight": "bold"}])

    credit(fig)
    return save_both(fig, f"{out_dir}/mexico_rsa_cards")


if __name__ == "__main__":
    print(main())
