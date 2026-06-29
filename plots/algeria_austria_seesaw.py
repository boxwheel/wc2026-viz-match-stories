"""Viz: Algeria 3-3 Austria — the see-saw thriller.

A diverging "lead ribbon": the home (Algeria) lead over Austria as a signed
quantity over time. Above the baseline = Algeria ahead, below = Austria ahead.
The chart crosses zero on every equaliser, peaks at each lead change, and
finishes pinned at zero by the 90'+ Austrian equaliser.
"""
from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
from highlight_text import fig_text

from data.load import match_brief, match_events_long
from style.house import apply_style, save_both, credit, INK, DIM, HOME, AWAY, BG, PANEL, ACCENT

MATCH_ID = 68


def main(out_dir: str = "artifacts") -> tuple[str, str]:
    apply_style()
    b = match_brief(MATCH_ID)
    e = match_events_long(MATCH_ID)
    goals = e[e.event_type == "Goal"].sort_values("minute").reset_index(drop=True)

    # build step series of (home - away) over time, with one event per goal
    xs, ys = [0], [0]
    h, a = 0, 0
    descs = [(0, "kickoff", 0)]
    for _, g in goals.iterrows():
        if g.side == "home":
            h += 1
        else:
            a += 1
        diff = h - a
        xs.append(g.minute); ys.append(ys[-1])      # hold
        xs.append(g.minute); ys.append(diff)        # jump
        descs.append((g.minute, f"{h}–{a}", diff))
    xs.append(95); ys.append(ys[-1])

    fig = plt.figure(figsize=(13, 7))
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0.07, 0.22, 0.86, 0.55])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 95)
    ax.set_ylim(-1.6, 1.6)

    # baseline + grid
    for x in (15, 30, 45, 60, 75, 90):
        ax.axvline(x, color=PANEL, lw=0.7, zorder=0)
        ax.text(x, -1.55, f"{x}'", color=DIM, fontsize=9, ha="center", va="top")
    ax.axvspan(45, 46.5, color=ACCENT, alpha=0.10, zorder=0)
    ax.text(45.7, 1.45, "HT", color=ACCENT, fontsize=9, va="top")
    ax.axhline(0, color=DIM, lw=0.8)

    # fill areas: blue when home ahead, amber when away ahead
    xa = np.array(xs); ya = np.array(ys)
    ax.fill_between(xa, 0, np.clip(ya, 0, None), step="pre", color=HOME, alpha=0.35)
    ax.fill_between(xa, 0, np.clip(ya, None, 0), step="pre", color=AWAY, alpha=0.35)
    ax.step(xa, ya, where="pre", color=INK, lw=1.6)

    # mark each goal with a labelled bubble
    for minute, label, diff in descs[1:]:
        side = "home" if (diff > descs[descs.index((minute, label, diff))-1][2]) else "away" if (diff < descs[descs.index((minute, label, diff))-1][2]) else "home"
        # actually simpler: figure scoring side from goals
        pass
    # repeat clean: use goals frame for labels
    h2, a2 = 0, 0
    for _, g in goals.iterrows():
        if g.side == "home":
            h2 += 1
        else:
            a2 += 1
        diff = h2 - a2
        col = HOME if g.side == "home" else AWAY
        y = diff
        ax.scatter(g.minute, y, s=260, color=col, edgecolor=INK, lw=1.4, zorder=5)
        ax.text(g.minute, y, f"{h2}–{a2}", color=INK, fontsize=10,
                fontweight="bold", ha="center", va="center", zorder=6)
        ax.text(g.minute, y + (0.30 if y >= 0 else -0.30),
                f"{g.minute}'", color=col, fontsize=9, ha="center",
                va="bottom" if y >= 0 else "top", fontweight="bold")

    # zone labels
    ax.text(2, 1.45, f"{b['home']} ahead", color=HOME, fontsize=10, va="top")
    ax.text(2, -1.45, f"{b['away']} ahead", color=AWAY, fontsize=10, va="bottom")
    for spine in ("top", "right", "left", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])

    # title block
    fig.text(0.07, 0.93, "The see-saw", color=INK, fontsize=24, fontweight="bold")
    fig_text(0.07, 0.87,
             f"<{b['home']}> 3–3 <{b['away']}> · {b['date']} · {b['stadium']}",
             color=DIM, fontsize=13,
             highlight_textprops=[{"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}], fig=fig)
    fig.text(0.07, 0.83,
             "Lead margin over 90'. The ribbon flips colour every time the lead changes hands.",
             color=DIM, fontsize=10.5)

    fig_text(0.07, 0.13,
             "Six goals, four lead changes. <Austria> took the lead twice and were minutes from a win "
             "after the <55'> strike; <Algeria>'s second-half comeback peaked at 3–2 with a 90' winner — "
             "answered by <Austria>'s instant equaliser to share the points.",
             color=INK, fontsize=11, fig=fig,
             highlight_textprops=[{"color": AWAY, "fontweight": "bold"},
                                  {"color": DIM, "fontweight": "bold"},
                                  {"color": HOME, "fontweight": "bold"},
                                  {"color": AWAY, "fontweight": "bold"}])

    credit(fig)
    return save_both(fig, f"{out_dir}/algeria_austria_seesaw")


if __name__ == "__main__":
    print(main())
