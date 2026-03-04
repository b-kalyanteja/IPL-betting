import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

from utils.players import player_map
from utils.sheets_data import df_02, df_07, df_05
from utils.betting_form import betting_manager

import random


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

