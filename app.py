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
    "seasons through three different perspectives: how team fortunes shifted between campaigns, "
    "how reliably teams can generate attacking threat from week to week, and — at the heart of it all — whether the home crowd still provides a real competitive edge. "
    "Navigate the pages in the sidebar to explore the full story:\n"
    "- **Central Narrative**: A guided, chart-driven story answering each of the three analytical questions.\n"
    "- **Exploration**: An open-ended interactive dashboard for reader-driven analysis.\n"
    "- **Methodology**: Key details about the data and the limits of our analysis.\n"
)

st.info("Data: Football-Data.co.uk — English Premier League match results, 2023–24 and 2024–25.")
st.divider()

