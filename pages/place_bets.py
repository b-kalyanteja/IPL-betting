import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

from utils.players import player_map
from utils.sheets_data import df_02, df_07, df_05
from utils.betting_form import betting_manager

st.set_page_config(
    page_title="🎰 Place Bets",
    page_icon=" 🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def clock_bar():
    # india_tz = pytz.timezone('Asia/Kolkata')
    # ist_now = datetime.now(india_tz).strftime("%H:%M:%S")
     st.markdown("### 🕒 Indian Time : ")
    # st.title(f"{ist_now}")
clock_bar()

st.divider()

# --- 2. LOGIN LOGIC  PRIVATE SESSION ---
if not st.user.get("is_logged_in"):
    # STATE 1: Not Logged In
    st.info("📍 Log in to place your bet!")
    if st.button("Log in with Google"):
        st.login("google")

else:
    current_email = st.user.get("email")

    if current_email not in player_map.keys():
        st.error(f" పోరా సన్నాసి 🤬🤬 {current_email} is not authorized to bet ")
        time.sleep(1)

        st.logout()
        st.rerun()
        st.stop()  #  CRITICAL: This kills the script here so the form never shows

    else:
        # STATE 3: Logged in and Authorized
        st.write(f" ✅ Active Player: **{current_email}**")

        if st.button("Log out"):
            st.session_state.clear()  # added newly
            st.logout()
            st.rerun()

        betting_manager(current_email)

st.divider()
