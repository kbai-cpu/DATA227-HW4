import streamlit as st

st.set_page_config(page_title="Methodology", layout="wide")

st.title("Methodology & Limitations")

st.subheader("Data Source")
st.write(
    "Match-level results for the English Premier League were sourced from "
    "[Football-Data.co.uk](https://www.football-data.co.uk/englandm.php), "
    "covering two complete seasons: 2023–24 and 2024–25. "
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
- **Points**: 3 for a win, 1 for a draw, 0 for a loss, computed separately for home and away appearances.
- **Goal Difference**: Goals scored minus goals conceded across all matches.
- **3-Match Rolling Average**: A rolling window of size 3 (minimum 1 period) applied per team per season to smooth per-match attacking stats.
- **Home Advantage**: Home points minus away points for a given team and season.
""")

st.subheader("Limitations")
st.markdown("""
- Our analysis is purely observational. We can only see association in the data, not causation. 
- We are working with only two seasons of data, and cannot treat short term patterns as long term trends. A team’s home advantage or attacking consistency could fluctuate significantly in future seasons.
- We cannot compare clubs that only appear in one season, which limits our ability to analyze promoted and relegated teams.
- We are using aggregate season-level metrics for the home vs away comparison, which may obscure important within-season variation in home advantage.
- The dataset excludes context. Injuries, suspensions, managerial changes, and other factors that influence performance are not captured in the data, but can significantly influence results.
""")
