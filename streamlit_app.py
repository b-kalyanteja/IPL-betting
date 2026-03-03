import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

from utils.sheets_data import df_02, df_07, df_05

from utils.betting_form import betting_manager
import random
# from utils import players

players = ["b.kalyanteja@gmail.com", "mvr08626@gmail.com", "sravanteja10@gmail.com", "narasimharao416@gmail.com", "jagadeeswarabojja@gmail.com", "gbmkrishnayadav@gmail.com"]
# CREATE connection to Google sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏆 2026 Betting Dashboard")



st.divider()

if not st.user.get("is_logged_in"):
    # STATE 1: Not Logged In
    st.info("Predictor's Dashboard")
    if st.button("Log in with Google"):
        st.login("google")
else:
    current_email = st.user.get("email")


st.divider()

# --- 2. LOGIN LOGIC  PRIVATE SESSION ---
if not st.user.get("is_logged_in"):
    # STATE 1: Not Logged In
    st.info("📍 Log in to place your bet!")
    if st.button("Log in with Google"):
        st.login("google")

else:
    current_email = st.user.get("email")

    if current_email not in players:
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

        # --- PROCEED WITH THE APP ---
        betting_manager(current_email, df_07, df_05, conn)

st.divider()

if not df_01.empty:
    # 1. Clean column names
    df_01.columns = [str(c).strip().lower() for c in df_01.columns]

    # 2. Convert Wager to numbers (so the chart handles it correctly)
    if "amount" in df_01.columns:
        df_01["amount"] = pd.to_numeric(df_01["amount"], errors='coerce').fillna(0)

        st.subheader("💰 Rolling amount ")
        # Identify the user column (usually the first column)
        user_col = df_01.columns[0]
        st.bar_chart(data=df_01, x=user_col, y="amount")
    else:
        st.error(f"Could not find 'amount' column. Found these instead: {list(df_01.columns)}")
else:
    st.info("No data found to graph yet.")
