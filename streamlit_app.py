import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from utils.match_display import display_matches
from utils.cumilative_graph import performance_graph, current_status, current_status_02
from utils.prediction_daily import today_prediction
import plotly.express as px


# CREATE connection to Google sheets
conn = st.connection("gsheets", type=GSheetsConnection)



st.set_page_config(
    page_title="IPL 2026 Bets",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🏆 IPL'26 Bets")

st.write("Today's matches")
display_matches()
st.divider()

today_prediction()
st.divider()

st.write("Player's Performance")
performance_graph()
st.divider()

#current_status() - it looks like table ... routine
#st.divider()

current_status_02()
st.divider()



