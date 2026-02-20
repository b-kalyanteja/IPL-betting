import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import random
# from utils import players

players = ["b.kalyanteja@gmail.com", "mvr08626@gmail.com", "sravanteja10@gmail.com", "narasimharao416@gmail.com", "jaggu"]
# CREATE connection to Google sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏆 2026 Betting Dashboard")

# --- LOAD DATA ---
df_01 = conn.read(worksheet="2026_summary", ttl=1)
df_02 = conn.read(worksheet="2026_bets",  ttl=1)




st.divider()

# --- 2. LOGIN LOGIC  PRIVATE SESSION ---
if not st.user.get("is_logged_in"):
    # STATE 1: Not Logged In
    st.subheader("📍 Place Your Bet")
    st.info("Log in to join the action!")
    if st.button("Log in with Google"):
        st.login("google")

else:
    current_email = st.user.get("email")

    if current_email not in players:
        st.error(f" పోరా సన్నాసి 🤬🤬 {current_email} is not authorized to bet ")
        time.sleep(0.5)

        st.logout()
        st.rerun()
        st.stop()  #  CRITICAL: This kills the script here so the form never shows

    else:
        # STATE 3: Logged in and Authorized
        st.write(f" ✅ Active Player: **{current_email}**")

        if st.button("Log out"):
            st.logout()
            st.rerun()

        # --- PROCEED WITH THE APP ---
        with st.form("betting_form"):
            choice = st.selectbox("Pick your team:", ["CSK", "MI"])
            amount = st.number_input("Bet Amount (Zl)", min_value=5, step=1, max_value=10)
            submit = st.form_submit_button("Lock Bet 🔒")

            if submit:
                # Your saving logic here...
                st.success("Bet placed!")
                st.balloons()

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