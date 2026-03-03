import streamlit as st
import altair as alt
from utils.io import load_pl_data
from charts.charts import (
    base_theme,
    chart_team_performance,
    chart_attacking_consistency,
    chart_home_advantage,
)

st.set_page_config(page_title="Exploration", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

team_summary_long, team_attack_long, q3_pivot = load_pl_data()

st.title("Interactive Exploration")
st.write(
    "The full dashboard below combines all three analytical views into one unified, "
    "reader-driven interface. Every interaction is connected: clicking a team in the "
    "season comparison at the top filters the attacking consistency panels in the middle, "
    "while the interval brush in the home/away scatter plot at the bottom independently "
    "updates the home advantage bar chart. Use the guided prompts below to structure your "
    "exploration, or simply follow your own curiosity."
)

st.markdown("**How to interact:**")
st.write(
    "- **Metric dropdown** (top chart): switch between Points, Wins, and Goal Difference "
    "to view season-over-season performance through different lenses.\n"
    "- **Click a line** (top chart): highlight a single team and see only that team's "
    "3-match rolling attack averages in the panels below it.\n"
    "- **Attacking Metric dropdown** (middle chart): toggle between Goals, Shots, and "
    "Shots on Target to probe different dimensions of attacking output.\n"
    "- **Drag a brush** (bottom scatter): select a cluster of teams by their home vs. away "
    "points to reveal how home advantage is distributed within that group across both seasons."
)

st.markdown("**Guided prompts:**")
st.write(
    "- Which teams sit furthest above the diagonal in the scatter plot — and does their "
    "home advantage hold across both seasons or only one?\n"
    "- Click a top-four team in the season comparison: does their attacking rolling average "
    "stay flat and consistent, or does it show mid-season dips?\n"
    "- Switch the metric to Goal Difference and compare it against Points — are there teams "
    "whose goal difference tells a sharply different story than their points tally?\n"
    "- Brush only the teams with high away points in the scatter: do those clubs also show "
    "lower home advantage in the bar chart, suggesting they are equally strong everywhere?"
)

st.divider()

q1_chart, team_select = chart_team_performance(team_summary_long)
q2_chart = chart_attacking_consistency(team_attack_long, team_select)
q3_chart = chart_home_advantage(q3_pivot)

final_dashboard = (
    alt.vconcat(q1_chart, q2_chart, q3_chart)
    .resolve_scale(color="independent")
)

st.altair_chart(final_dashboard, use_container_width=True)
