# WC-2026 Match Stories — per-match data visualizations

One striking visualization per dramatic match from the **FIFA World Cup 2026**
group stage, built from post-match events (goals, cards, VAR), team stats
(possession, shots, xG totals) and lineups. Lives inside the broader Flywheel
visualization graph.

## What's in here

```
data/         tidy CSV loaders (matches, events, team_stats, lineups)
style/        house.py — shared dark editorial matplotlib theme
transforms/   match.py — running score, xG path, momentum series
plots/        one module per visualization — each writes PNG@200dpi + SVG
artifacts/    rendered outputs (kept under git so the repo is self-contained)
```

## Reproduce

```bash
uv venv .venv --python 3.12 && . .venv/bin/activate
uv pip install pandas numpy matplotlib seaborn mplsoccer plotnine highlight-text pyarrow scipy
# fetch dataset to ~/research/fifa_data (see scripts/fetch_data.sh)
python -m plots.<name>
```

Every plot module is a single `python -m plots.<name>` entrypoint that reads
from `~/research/fifa_data/*.csv` and writes both formats into `artifacts/`.

## Honesty notes

- The dataset publishes **match xG totals only**, not per-shot xG. The "xG path"
  charts use a linear interpolation anchored to those totals — they are a
  *tempo proxy*, not a per-shot trace, and are labelled as such on the chart.
- No shot location coordinates are in the dataset, so we don't fabricate a
  literal shot map; the mplsoccer pitch is used as a canvas for event timelines.

## Flywheel

Root: `red-grass-3094` (`8ee1400c-a376-5b44-b10a-e1f50f0cfc82`).  
Lane: per-match stories, Cluster `Match-Stories`. Each visualization is one
multi-parent leaf scored against the project's 5-axis rubric.
