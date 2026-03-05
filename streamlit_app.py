import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from utils.match_display import match_widget_01, match_widget_02

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


match_widget_01(team_1 = "kkr", team_2 = "rcb", t1_bets =3,t2_bets=2)
match_widget_02(team_1 = "kkr", team_2 = "rcb", t1_bets =3,t2_bets=2)