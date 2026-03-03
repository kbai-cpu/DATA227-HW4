import streamlit as st
from PIL import Image

st.set_page_config(page_title="The Fortress Factor", layout="wide")

st.title("The Fortress Factor: Home Advantage and the Premier League's Two-Season Story")
st.image(Image.open('images/liverpool-arsenal.jpg'), use_container_width=True)

st.markdown("""
*In an era of billionaire owners, elite recruitment, and relentless tactical evolution, one
question cuts to the heart of English football: does playing at home still matter — and if so,
for whom?*
""")

st.write(
    "This project investigates Premier League performance across the **2023–24** and **2024–25** "
    "seasons through three interconnected lenses: how team fortunes shifted between campaigns, "
    "how reliably clubs could manufacture attacking threat from one week to the next, and — "
    "at the centre of it all — whether the home crowd remains a genuine competitive weapon. "
    "Navigate the pages in the sidebar to explore the full story:\n"
    "- **Central Narrative**: A guided, chart-driven story answering each of the three analytical questions.\n"
    "- **Exploration**: An open-ended interactive dashboard for reader-driven discovery.\n"
    "- **Methodology**: Key details about the data and the limits of our analysis.\n"
)

st.info("Data: Football-Data.co.uk — English Premier League match results, 2023–24 and 2024–25.")
