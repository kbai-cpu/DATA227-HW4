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
    "- Which teams sit furthest above the diagonal in the scatter plot showing Home vs Away performance, and does their "
    "home advantage hold across both seasons or only one?\n"
    "- Among the top four teams in the seasonal performance comparison: does their attacking rolling average stay flat and consistent, or does it show mid-season dips?\n"
    "- Are there teams whose goal difference tells a different story than their points tally? In other words, are there teams that are more dominant in terms of goal difference but less successful in terms of points?\n"
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
