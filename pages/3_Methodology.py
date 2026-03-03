import streamlit as st

st.set_page_config(page_title="Methodology", layout="wide")

st.title("Methodology & Limitations")

st.subheader("Data Source")
st.write(
    "Match-level results for the English Premier League were sourced from "
    "[Football-Data.co.uk](https://www.football-data.co.uk/englandm.php), "
    "covering two complete seasons: **2023–24** and **2024–25**. "
    "Each row in the raw data represents a single match."
)

st.subheader("Variables Used")
st.markdown("""
| Column | Description |
|--------|-------------|
| `HomeTeam` / `AwayTeam` | Club names for each fixture |
| `FTHG` / `FTAG` | Full-time home and away goals |
| `FTR` | Full-time result (`H` = home win, `A` = away win, `D` = draw) |
| `HS` / `AS` | Total shots (home / away) |
| `HST` / `AST` | Shots on target (home / away) |
| `HC` / `AC` | Corner kicks (home / away) |
| `Date` | Match date, used to order matchweeks within each season |
""")

st.subheader("Derived Metrics")
st.markdown("""
- **Points**: 3 for a win, 1 for a draw, 0 for a loss — computed separately for home and away appearances.
- **Goal Difference**: Goals scored minus goals conceded across all matches.
- **3-Match Rolling Average**: A rolling window of size 3 (minimum 1 period) applied per team per season to smooth per-match attacking stats.
- **Home Advantage**: Home points minus away points for a given team and season.
""")

st.subheader("Limitations")
st.markdown("""
- **Only two seasons of data.** Patterns observed here — particularly in home advantage — may not reflect long-term structural tendencies for any given club.
- **Promoted and relegated teams differ between seasons.** Clubs that were not present in both campaigns (e.g., promoted sides) cannot be meaningfully compared across seasons and will appear in only one season's panels.
- **Points-based home advantage is a blunt instrument.** It captures outcomes but not the mechanisms behind them — travel fatigue, crowd size, referee bias, and pitch familiarity all contribute to home advantage in ways this data cannot isolate.
- **Rolling averages at the start of a season are noisy.** Because `min_periods=1` is used, matchweek 1 and 2 values are based on one or two games respectively and should be interpreted cautiously.
- **No contextual match information.** Injuries, suspensions, fixture congestion, and managerial changes are not accounted for and can substantially affect individual match results.
- **Observational data only.** All relationships identified (e.g., between home points and home advantage) are associational, not causal.
""")
