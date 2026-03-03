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
    "The full dashboard brings all three views together in one place. You can follow the prompts below to guide your analysis, or simply explore the patterns on your own."
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
