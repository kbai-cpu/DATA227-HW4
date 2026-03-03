import streamlit as st
import altair as alt
from PIL import Image
from utils.io import load_pl_data
from charts.charts import (
    base_theme,
    chart_team_performance,
    chart_attacking_consistency,
    chart_home_advantage,
)

st.set_page_config(page_title="The Fortress Factor", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

team_summary_long, team_attack_long, q3_pivot = load_pl_data()

# intro and title
st.title("The Fortress Factor: Home Advantage and the Premier League's Two-Season Story")
st.image(Image.open('images/liverpool-arsenal.jpg'), use_container_width=True)

st.markdown("""
*As billionaire owners, elite recruitment, and relentless tactical evolution reshape English football, one question remains worth asking: does playing at home still matter — and if so, for whom?*
""")

st.write(
    "This project investigates Premier League performance across the **2023–24** and **2024–25** "
    "seasons through three interconnected lenses: how team fortunes shifted between campaigns, "
    "how reliably clubs could manufacture attacking threat from one week to the next, and — "
    "at the centre of it all — whether the home crowd remains a genuine competitive weapon. "
    "Navigate the pages in the sidebar to explore the full story:\n"
    "- **Central Narrative** (this page): A guided, chart-driven story answering each of the three analytical questions.\n"
    "- **Exploration**: An open-ended interactive dashboard for reader-driven discovery.\n"
    "- **Methodology**: Key details about the data and the limits of our analysis.\n"
)

st.info("Data: Football-Data.co.uk — English Premier League match results, 2023–24 and 2024–25.")
st.divider()

# Question 1
st.header("1 — The Shifting Table: How Did Teams Change Between Seasons?")
st.markdown("""
The 2023–24 season was one of historic near-misses. Arsenal's 89-point campaign would have
won the title in almost any other year of the Premier League era — yet it still fell short.
One season later, the landscape had reorganised. Some clubs tightened their grip; others
surrendered ground they had spent years accumulating.

Use the **Metric** dropdown to switch between points, wins, and goal difference. Each lens
surfaces a slightly different truth about who genuinely improved and who merely clung on.
**Click any line to highlight a single team** and carry that selection into the attacking
consistency chart below.
""")

q1_chart, team_select = chart_team_performance(team_summary_long)

# Question 2 
st.header("2 — Pulse Check: How Consistent Is a Team's Attack Within a Season?")
st.markdown("""
A single brilliant result can flatter any side. What separates genuine contenders from
flattering pretenders is the capacity to manufacture danger and goals week after week —
regardless of opponent, venue, or circumstance.

The rolling-average lines below smooth out the noise of individual results and expose the
underlying rhythm of each team's attack across both seasons, split into side-by-side panels.
**Select a team in the chart above** to filter both season panels here simultaneously, then
toggle the **Attacking Metric** dropdown to compare goals, total shots, and shots on target.
""")

q2_chart = chart_attacking_consistency(team_attack_long, team_select)

st.altair_chart(q1_chart & q2_chart, use_container_width=True)

st.divider()

# Question 3 
st.header("3 — Home Truths: Where the Fortress Holds and Where It Doesn't")
st.markdown("""
Not every stadium is a fortress. For some clubs, home fixtures are near-guarantees — opponents
wilt under crowd noise, familiar turf, and the psychological weight of expectation. For others,
the home–away split barely registers; they are just as formidable on the road.

The scatter plot below makes this structural divide visible at a glance: **teams above the
diagonal earn more points at home than away**. Use the interval brush to select a cluster of
teams, and watch the grouped bar chart below update to show exactly how large — or surprisingly
small — each club's home advantage is, with both seasons shown side by side so you can judge
whether the gap widened, narrowed, or held steady.
""")

st.altair_chart(chart_home_advantage(q3_pivot), use_container_width=True)
