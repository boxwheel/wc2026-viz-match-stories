"""Viz: Norway 1-4 France — the night xG and the scoreboard disagreed.

Norway out-shot France in xG (1.30 vs 0.96) yet lost 1-4. The chart is a
diverging arrow pair: from each team's xG total (the dim baseline) to their
actual goals (the bright endpoint). When the arrow shoots way past xG, the
team massively over-performed; when it falls short, they under-performed.
Below: the goal timeline as a one-line strip — France's 7' opener and three
quick goals before half-time, Norway's late consolation.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
from highlight_text import fig_text

from data.load import match_brief, match_events_long
from style.house import apply_style, save_both, credit, INK, DIM, HOME, AWAY, BG, PANEL, ACCENT, GOOD, BAD

MATCH_ID = 65


def main(out_dir: str = "artifacts") -> tuple[str, str]:
    apply_style()
    b = match_brief(MATCH_ID)
    e = match_events_long(MATCH_ID)
    goals = e[e.event_type == "Goal"]

    fig = plt.figure(figsize=(12.5, 8))
    fig.patch.set_facecolor(BG)

    # ---- top: divergence arrows ----
    ax = fig.add_axes([0.10, 0.40, 0.82, 0.36])
    ax.set_facecolor(BG)

    rows = [
        ("home", b["home"], b["home_xg"], b["home_score"]),
        ("away", b["away"], b["away_xg"], b["away_score"]),
    ]
    max_v = max(b["home_score"], b["away_score"], b["home_xg"], b["away_xg"]) + 0.6

    for i, (side, name, xg, gls) in enumerate(rows):
        y = 1 - i
        col = HOME if side == "home" else AWAY
        # xG baseline marker
        ax.plot([xg, xg], [y - 0.18, y + 0.18], color=DIM, lw=2, alpha=0.7)
        ax.text(xg, y + 0.30, f"xG {xg:.2f}", color=DIM, fontsize=10, ha="center", va="bottom")
        # arrow from xG to actual goals
        arrow_col = GOOD if gls > xg else BAD
        ax.annotate(
            "", xy=(gls, y), xytext=(xg, y),
            arrowprops=dict(arrowstyle="-|>,head_width=0.5,head_length=0.8",
                            color=arrow_col, lw=4, shrinkA=0, shrinkB=0),
        )
        ax.scatter(gls, y, s=420, color=col, edgecolor=INK, lw=1.5, zorder=4)
        ax.text(gls, y, f"{gls}", color=INK, fontsize=16, fontweight="bold",
                ha="center", va="center", zorder=5)
        # team label
        ax.text(-0.25, y, name, color=col, fontsize=15, fontweight="bold",
                ha="right", va="center")
        # delta
        delta = gls - xg
        sign = "+" if delta >= 0 else ""
        ax.text(max_v + 0.05, y, f"{sign}{delta:.2f}  vs xG",
                color=arrow_col, fontsize=11, fontweight="bold", ha="left", va="center")

    ax.set_xlim(-0.05, max_v + 0.9)
    ax.set_ylim(-0.7, 1.7)
    # x axis ticks
    ax.set_xticks(range(0, int(max_v) + 1))
    ax.set_xticklabels([str(i) for i in range(int(max_v) + 1)])
    ax.set_yticks([])
    ax.set_xlabel("goals (expected · actual)", color=DIM, fontsize=10)
    ax.tick_params(colors=DIM)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(PANEL)

    # ---- bottom: goal timeline ----
    ax2 = fig.add_axes([0.10, 0.16, 0.82, 0.12])
    ax2.set_facecolor(BG)
    ax2.set_xlim(0, 95)
    ax2.set_ylim(-0.8, 0.8)
    ax2.axhline(0, color=DIM, lw=0.6)
    ax2.axvline(45, color=DIM, ls=(0, (4, 4)), lw=0.5)
    ax2.text(45.5, 0.7, "HT", color=DIM, fontsize=9, va="top")
    for _, g in goals.iterrows():
        col = HOME if g.side == "home" else AWAY
        y = 0.4 if g.side == "home" else -0.4
        ax2.scatter(g.minute, y, s=140, color=col, edgecolor=INK, lw=1.2)
        ax2.text(g.minute, y + (0.25 if y > 0 else -0.25),
                 f"{g.minute}'", color=col, fontsize=9, ha="center",
                 va="bottom" if y > 0 else "top", fontweight="bold")
    for x in (15, 30, 45, 60, 75, 90):
        ax2.text(x, -0.78, f"{x}'", color=DIM, fontsize=9, ha="center", va="top")
    for sp in ax2.spines.values():
        sp.set_visible(False)
    ax2.set_xticks([]); ax2.set_yticks([])

    # title block
    fig.text(0.10, 0.92, "When xG and the scoreboard disagree", color=INK,
             fontsize=22, fontweight="bold")
    fig_text(0.10, 0.87,
             f"<{b['home']}> 1–4 <{b['away']}> · {b['date']} · {b['stadium']}",
             color=DIM, fontsize=13,
             highlight_textprops=[{"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}], fig=fig)
    fig.text(0.10, 0.83,
             "Each arrow goes from a team's published xG to their actual goal count. Up-shoot = clinical; under-shoot = wasteful.",
             color=DIM, fontsize=10.5)

    fig_text(0.10, 0.08,
             "<France> had a lower xG (0.96) than <Norway> (1.30) yet scored four times — every shot a brutal payout. "
             "Norway out-chanced them on the board and were 3.04 goals below their xG.",
             color=INK, fontsize=11, fig=fig,
             highlight_textprops=[{"color": AWAY, "fontweight": "bold"},
                                  {"color": HOME, "fontweight": "bold"}])

    credit(fig)
    return save_both(fig, f"{out_dir}/norway_france_xg_inversion")


if __name__ == "__main__":
    print(main())
