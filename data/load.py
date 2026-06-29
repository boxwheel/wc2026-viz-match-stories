"""Load FIFA WC-2026 tidy frames from ~/research/fifa_data."""
from __future__ import annotations
import os
from pathlib import Path
import pandas as pd

DATA_DIR = Path(os.environ.get("FIFA_DATA", Path.home() / "research" / "fifa_data"))


def _csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


def matches() -> pd.DataFrame:
    m = _csv("matches.csv")
    md = _csv("matches_detailed.csv")
    st = _csv("tournament_stages.csv")
    out = (m.merge(md.drop(columns=["date", "kickoff_time_utc", "status",
                                    "home_score", "away_score", "home_xg", "away_xg"]),
                   on="match_id")
            .merge(st, on="stage_id"))
    return out


def teams() -> pd.DataFrame:
    return _csv("teams.csv")


def events() -> pd.DataFrame:
    return _csv("match_events.csv")


def team_stats() -> pd.DataFrame:
    return _csv("match_team_stats.csv")


def lineups() -> pd.DataFrame:
    return _csv("match_lineups.csv")


def players() -> pd.DataFrame:
    return _csv("squads_and_players.csv")


def venues() -> pd.DataFrame:
    return _csv("venues.csv")


def match_brief(match_id: int) -> dict:
    """Return a tight dict describing one match — used for chart titles."""
    m = matches().query("match_id == @match_id").iloc[0]
    return {
        "match_id": int(match_id),
        "date": str(m.date),
        "home": m.home_team_name,
        "away": m.away_team_name,
        "home_id": int(m.home_team_id),
        "away_id": int(m.away_team_id),
        "home_score": int(m.home_score),
        "away_score": int(m.away_score),
        "home_xg": float(m.home_xg),
        "away_xg": float(m.away_xg),
        "stage": m.stage_name_x if "stage_name_x" in m else m.get("stage_name"),
        "stadium": m.stadium_name,
        "city": m.city,
    }


def match_events_long(match_id: int) -> pd.DataFrame:
    e = events().query("match_id == @match_id").copy()
    b = match_brief(match_id)
    e["side"] = e["team_id"].map({b["home_id"]: "home", b["away_id"]: "away"})
    e["team_name"] = e["team_id"].map({b["home_id"]: b["home"], b["away_id"]: b["away"]})
    return e.sort_values("minute").reset_index(drop=True)
