import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from utils.match_display import match_widget

# PREDICTION columns ()


# Funtion to show next match bet's status .. How many players on each team . .
'''
count how many on each side and then update the Diagram for the latest match
'''


# Daily Cumilative graph

# CREATE connection to Google sheets
conn = st.connection("gsheets", type=GSheetsConnection)



st.set_page_config(
    page_title="IPL 2026 Bets",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🏆 IPL'26 Bets")

st.divider()


match_widget(team1_name = "kkr", team1_logo = "🔫", team2_name = "RCB", team2_logo = "🧞‍♂️", bets_t1 = 3, bets_t2 = 2)