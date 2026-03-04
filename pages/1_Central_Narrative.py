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
- Arsenal’s drop from 89 points to 74 was the sharpest decline among the established top clubs. But when you switch to goal difference, their +62 in 2023–24 dropped to +35 in 2024–25, making their fall look more pronounced.
- Several mid-table teams moved in the opposite direction. Brentford improved by 17 points and Brighton by 13.
- Overall, the 2024–25 season appears just slightly more compressed, with more clubs clustered around the mid-50s in points. The gap between the top and the rest seems to have narrowed compared to the previous year.
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
- Even the strongest attacking teams show significant week-to-week volatility in the rolling averages. Truly flat, sustained output is rare, and most teams exhibit clear peaks and troughs within a single season.
- Consistent mid-season dips across many teams likely reflect fixture congestion, injuries, or short-term drops in form. The rolling average makes these broader patterns visible while smoothing out the noise of individual matches. 
""")

st.divider()

# Question 3 
st.header("3 — Home Advantage: Where It Holds and Where It Weakens")
st.markdown("""
Home advantage is not uniform across clubs. For some, home games consistently yield stronger results, suggesting that factors such as crowd support, familiarity with the environment, and contextual factors meaningfully influence performance. For others, the difference between home and away outcomes is minimal, indicating a more stable level of performance across venues.

The scatter plot below shows home points on the x-axis and away points on the y-axis, with each point representing a team’s performance in one season. The diagonal line represents parity between home and away points; teams above the line perform better away than at home, while those below it benefit more from home advantage. You can drag a brush to select a cluster of teams and see how their home advantage is distributed in the bar chart below the scatterplot.

""")

st.altair_chart(chart_home_advantage(q3_pivot), use_container_width=True)

st.markdown("""
**Key takeaways:**
- The majority of teams cluster above the diagonal, confirming that home advantage is real and widespread across the Premier League. For the majority of clubs, scoring points away from home is simply harder. 
- Teams like Arsenal, Brentford, and Man United are notable exceptions. Their home advantages are only about 4–6 points in both seasons, meaning they perform almost as well on the road as they do at home.
- Aston Villa, on the other hand, show one of the largest home–away gaps: 12 points in 2023–24 and 14 in 2024–25. Moreover, their home advantage appears to have strengthened in the second season, suggesting that their home ground is a key driver of their overall performance.
- Some teams (Brighton, Newcastle, Liverpool) had sharp dips in home advantage from 2023–24 to 2024–25, while others (Man City) had a notable increase. These shifts suggest that home advantage is not a fixed trait for any given club, but can fluctuate based on changes in squad, tactics, or other contextual factors.
- Many teams (Aston Villa, Chelsea, Man United, Brentford, Arsenal) show fairly stable home advantage across the two seasons. If this pattern holds in the long run, it suggests that home advantage is a structural feature of certain clubs rather than a transient phenomenon.
""")

