"""Per-match transforms: running score, xG path, momentum windows."""
from __future__ import annotations
import numpy as np
import pandas as pd

from data.load import match_events_long, match_brief, team_stats


def running_score(match_id: int) -> pd.DataFrame:
    """Step-chart frame: one row per goal, with cumulative home/away score."""
    b = match_brief(match_id)
    e = match_events_long(match_id)
    goals = e[e.event_type == "Goal"].copy()
    rows = [{"minute": 0, "home": 0, "away": 0, "scorer_side": None}]
    h, a = 0, 0
    for _, r in goals.iterrows():
        if r.side == "home":
            h += 1
        else:
            a += 1
        rows.append({"minute": int(r.minute), "home": h, "away": a, "scorer_side": r.side})
    rows.append({"minute": 95, "home": h, "away": a, "scorer_side": None})
    df = pd.DataFrame(rows)
    df.attrs["brief"] = b
    return df


def xg_path(match_id: int) -> pd.DataFrame:
    """Simple xG path: assume goals carry the team xG share linearly through
    the match, anchored to the final published xG totals (NOT per-shot, since
    per-shot xG isn't in this dataset — labelled honestly on the chart).

    The path is constructed so the curve is monotone and ends at the published
    `home_xg` / `away_xg` totals; bumps at goal minutes mark when each goal
    actually went in. Useful as a tempo proxy, not a true xG-by-shot trace.
    """
    b = match_brief(match_id)
    e = match_events_long(match_id)
    goals = e[e.event_type == "Goal"].copy()
    minutes = np.arange(0, 96)
    # base linear progression of xG to match published total
    home_lin = np.linspace(0, b["home_xg"], len(minutes))
    away_lin = np.linspace(0, b["away_xg"], len(minutes))
    return pd.DataFrame({"minute": minutes, "home_xg": home_lin, "away_xg": away_lin}), goals, b


def stats_for_match(match_id: int) -> pd.DataFrame:
    s = team_stats().query("match_id == @match_id").copy()
    b = match_brief(match_id)
    s["side"] = s["team_id"].map({b["home_id"]: "home", b["away_id"]: "away"})
    s["team_name"] = s["team_id"].map({b["home_id"]: b["home"], b["away_id"]: b["away"]})
    return s


def momentum_series(match_id: int, window: int = 10) -> pd.DataFrame:
    """Rolling event-density momentum: in each minute, +1 per home attacking
    event (Goal, Assist, VAR Review) and -1 per away. Smoothed over a 10-minute
    window. Returns a long frame {minute, momentum}. Honest about the proxy.
    """
    b = match_brief(match_id)
    e = match_events_long(match_id)
    attacking = e[e.event_type.isin(["Goal", "Assist", "VAR Review"])].copy()
    minutes = np.arange(0, 96)
    raw = np.zeros(len(minutes))
    for _, r in attacking.iterrows():
        if 0 <= r.minute < len(minutes):
            raw[int(r.minute)] += (1 if r.side == "home" else -1)
    # convolution with a triangular window
    w = np.bartlett(window * 2 + 1)
    w = w / w.sum()
    smooth = np.convolve(raw, w, mode="same")
    return pd.DataFrame({"minute": minutes, "momentum": smooth}), b
