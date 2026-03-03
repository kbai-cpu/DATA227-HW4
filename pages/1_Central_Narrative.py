import streamlit as st
import altair as alt
from utils.io import load_pl_data
from charts.charts import (
    base_theme,
    chart_team_performance,
    chart_attacking_consistency,
    chart_home_advantage,
)

st.set_page_config(page_title="Story", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

team_summary_long, team_attack_long, q3_pivot = load_pl_data()

# Question 1 
st.header("1 — The Shifting Table: How Did Team Performance Change Between Seasons?")
st.markdown("""
The 2023–24 season was defined by a historic near-miss. Arsenal’s 89-point total would have secured the Premier League title in most seasons, yet it proved insufficient in this competitive context. One year later, the competitive landscape had shifted. Certain clubs consolidated their positions, while others relinquished advantages that had taken multiple seasons to build.

The Metric dropdown allows you to switch between points, wins, and goal difference. Each measure offers a distinct perspective on performance: points capture the ultimate outcome, wins reflect consistency in securing results, and goal difference reveals underlying dominance or vulnerability.
Click any line to highlight a single team and carry that selection into the attacking
consistency chart below.
""")

q1_chart, team_select = chart_team_performance(team_summary_long)

st.altair_chart(q1_chart, use_container_width=True)

st.markdown("""
**Key takeaways:**
- Arsenal's 15-point drop (89 → 74) was the steepest decline among established top clubs, but switching the metric to Goal Difference tells an even starker story — their +62 margin in 2023–24 fell to +35 in 2024–25, suggesting the underlying erosion was greater than the headline points figure implies.
- Several mid-table clubs showed the largest upward trajectories: Brentford gained 17 points and Brighton gained 13 between seasons, pointing to improving squads rather than top-heavy variance.
- Goal Difference frequently reveals a sharper picture of team quality than points alone. A side can hold its points total through narrow wins while quietly conceding more — a warning sign that the raw table obscures.
- The field compressed noticeably in 2024–25, with more clubs clustering in the mid-50s points range, suggesting the gap between the top and the rest narrowed compared to the prior season.
""")

# Question 2
st.header("2 — How Consistent Is a Team's Attack Within a Season?")
st.markdown("""
A single standout performance can make any team look stronger than it truly is. What distinguishes genuine contenders is the ability to consistently create chances and score goals from week to week regardless of opponent, venue, or circumstance.

The rolling averages below smooth out the volatility of individual matches, revealing the underlying pattern of each team’s attacking output across both seasons in side-by-side panels. You can select a team in the chart above to filter both panels simultaneously, and use the Attacking Metric dropdown to compare goals, total shots, and shots on target.
""")

q2_chart = chart_attacking_consistency(team_attack_long, team_select)

st.altair_chart(q1_chart & q2_chart, use_container_width=True)

st.markdown("""
**Key takeaways:**
- Even top attacking sides show significant week-to-week volatility in the rolling averages — truly flat, sustained output is rare, and most teams exhibit clear peaks and troughs within a single season.
- Toggling from Goals to Shots exposes finishing efficiency. A team running a high shot rolling average alongside a low goals average is generating chances but not converting them — a pattern that often foreshadows a correction in results.
- Comparing the same metric across the two season panels reveals whether a team's attacking improvement or decline was real: clubs that genuinely strengthened tend to show a higher rolling average floor in 2024–25, meaning even their worst three-match stretches produced more than comparable low points in 2023–24.
- Mid-season dips in the rolling average are common across the board, likely reflecting fixture congestion, injuries, and form slumps — the smoothed line makes these structural dips visible where raw match-by-match data would obscure them.
""")

st.divider()

# Question 3 
st.header("3 — Home Advantage: Where It Holds and Where It Weakens")
st.markdown("""
Home advantage is not uniform across clubs. For some, home fixtures consistently yield stronger results, suggesting that factors such as crowd support, familiarity with the environment, and contextual pressures meaningfully influence performance. For others, the difference between home and away outcomes is minimal, indicating a more stable level of performance across settings.

The scatter plot below shows home points on the x-axis and away points on the y-axis, with each point representing a team’s performance in one season. The diagonal line represents parity between home and away points; teams above the line perform better away than at home, while those below it benefit more from home advantage. You can drag a brush to select a cluster of teams and see how their home advantage is distributed in the bar chart below the scatterplot.

""")

st.altair_chart(chart_home_advantage(q3_pivot), use_container_width=True)

st.markdown("""
**Key takeaways:**
- The majority of teams cluster above the diagonal, confirming that home advantage is real and widespread across the Premier League — accumulating points on the road is structurally harder for most clubs.
- Arsenal stand out as a clear outlier: with a home advantage of just 4–5 points across both seasons, they perform nearly as well away as at home, a hallmark of genuine elite-level consistency rather than fortress dependence.
- Aston Villa register one of the largest home advantages in the dataset — 12 points in 2023–24 and 14 in 2024–25 — and crucially, the gap grew rather than shrank between seasons, suggesting Villa Park is a durable structural asset, not a one-year anomaly.
- The side-by-side bars for each team reveal that home advantage is largely stable across both seasons for most clubs. Where it is consistent, it is likely organisational — rooted in crowd atmosphere, familiarity, and travel burden on opponents — rather than a product of luck or scheduling.
""")

