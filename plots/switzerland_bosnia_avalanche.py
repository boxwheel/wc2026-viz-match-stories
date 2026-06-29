"""Viz: Switzerland 4-1 Bosnia & Herzegovina — late avalanche.

Match 28 (2026-06-18). All four Switzerland goals fell at 80'+ after a Bosnian
red card. The chart shows the running score-line as a stepped area, with the
red-card moment marked as the inflection point and the goals annotated. A
small inset shows the per-15-minute shot share, dramatizing how the match
broke open.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
from highlight_text import fig_text

from data.load import match_brief, match_events_long, team_stats
from transforms.match import running_score
from style.house import apply_style, save_both, credit, INK, DIM, HOME, AWAY, BG, PANEL, ACCENT, BAD

MATCH_ID = 28


def main(out_dir: str = "artifacts") -> tuple[str, str]:
    apply_style()
    b = match_brief(MATCH_ID)
    e = match_events_long(MATCH_ID)
    rs = running_score(MATCH_ID)

    fig = plt.figure(figsize=(12.5, 7.2))
    fig.patch.set_facecolor(BG)

    ax = fig.add_axes([0.07, 0.16, 0.86, 0.58])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 95)
    ax.set_ylim(-0.4, max(rs.home.max(), rs.away.max()) + 1.4)

    # Step plots
    ax.step(rs.minute, rs.home, where="post", color=HOME, lw=3, label=b["home"])
    ax.step(rs.minute, rs.away, where="post", color=AWAY, lw=3, label=b["away"])
    ax.fill_between(rs.minute, 0, rs.home, step="post", color=HOME, alpha=0.13)
    ax.fill_between(rs.minute, 0, rs.away, step="post", color=AWAY, alpha=0.13)

    # half time marker
    ax.axvline(45, color=DIM, lw=0.6, ls=(0, (4, 4)))
    ax.text(45.6, ax.get_ylim()[1] - 0.2, "HT", color=DIM, fontsize=9, va="top")

    # mark red card
    red = e[e.event_type == "Red Card"]
    for _, r in red.iterrows():
        ax.axvline(r.minute, color=BAD, lw=1.4, alpha=0.85)
        ax.text(r.minute + 0.6, ax.get_ylim()[1] - 0.4,
                f"{r.minute}'  RED · {b['away']}", color=BAD, fontsize=10,
                fontweight="bold", va="top")

    # mark each goal with a dot
    goals = e[e.event_type == "Goal"]
    for _, g in goals.iterrows():
        side = g.side
        y = rs[(rs.minute == g.minute) & (rs.scorer_side == side)][side].iloc[0]
        col = HOME if side == "home" else AWAY
        ax.scatter(g.minute, y, s=80, color=col, edgecolor=INK, lw=1.2, zorder=5)
        ax.text(g.minute, y + 0.25, f"{g.minute}'", color=col, fontsize=9,
                ha="center", va="bottom", fontweight="bold")

    # axis cosmetics
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_xticklabels(["0'", "15'", "30'", "45'", "60'", "75'", "90'"])
    ax.set_yticks(range(0, int(ax.get_ylim()[1]) + 1))
    ax.tick_params(colors=DIM)
    ax.grid(axis="y", color=PANEL, lw=0.8)

    # right-edge final labels
    ax.text(93, rs.home.iloc[-1], f"  {rs.home.iloc[-1]}", color=HOME, fontsize=22,
            fontweight="bold", va="center")
    ax.text(93, rs.away.iloc[-1], f"  {rs.away.iloc[-1]}", color=AWAY, fontsize=22,
            fontweight="bold", va="center")

    # title block
    fig.text(0.07, 0.93, "The avalanche", color=INK, fontsize=24, fontweight="bold")
    fig_text(0.07, 0.87,
             f"<{b['home']}> 4–1 <{b['away']}> · {b['date']} · {b['stadium']}",
             color=DIM, fontsize=13,
             highlight_textprops=[{"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}], fig=fig)
    fig.text(0.07, 0.83,
             "Cumulative goals over 90'. Dots mark each goal; the red line is the red card.",
             color=DIM, fontsize=10.5)

    # Bottom annotation telling the story
    late = (e[(e.event_type == "Goal") & (e.minute >= 80)]
              .groupby("side").size().to_dict())
    fig_text(0.07, 0.08,
             f"At 80' the score was <1–0> and the match still open. A <{b['away']}> red card opened the floodgates: "
             f"<{b['home']}> scored <three more goals in ten minutes> "
             "to turn a tense contest into a procession.",
             color=INK, fontsize=11, fig=fig,
             highlight_textprops=[{"color": DIM, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"},
                                  {"color": HOME, "fontweight": "bold"},
                                  {"color": HOME, "fontweight": "bold"}])

    credit(fig)
    return save_both(fig, f"{out_dir}/switzerland_bosnia_avalanche")


if __name__ == "__main__":
    print(main())
