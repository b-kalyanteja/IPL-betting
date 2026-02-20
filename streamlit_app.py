import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from utils.verify_user import verify_user

# CREATE connection to Google sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏆 2026 Betting Dashboard")

# --- LOAD DATA ---
df_01 = conn.read(worksheet="2026_summary", ttl=1)
df_02 = conn.read(worksheet="2026_bets",  ttl=1)

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


st.divider()

# --- 2. LOGIN LOGIC  PRIVATE SESSION ---
if not st.user.get("is_logged_in"):
    st.subheader("📍 Place Your Bet")
    st.info("Log in to join the action!")
    if st.button("Log in with Google"):
        st.login("google")
else:
    # Get the email safely from the st.user object
    current_email = st.user.get("email")

    if current_email:
        # Pass the email variable, NOT st.email
        verify_user(current_email)

        st.write(f"Logged in as: **{current_email}**")

        if st.button("Log out"):
            st.logout()
            st.rerun()

        with st.form("betting_form"):
            choice = st.selectbox("Pick your team:", ["CSK", "MI"])
            amount = st.number_input("Bet Amount (Zl)", min_value=5, step=1, max_value=10)

            # This must be the form submit button
            submit = st.form_submit_button("Lock Bet 🔒")

            if submit:
                new_bet = pd.DataFrame([{"Email": current_email, "Choice": choice, "Wager": amount}])
                updated_df = pd.concat([df_02, new_bet], ignore_index=True)
                conn.update(worksheet="2026_bets", data=updated_df)

                st.balloons()
                st.success("Bet saved!")
                st.rerun()