import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# CREATE connection to Google sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏆 2026 Betting Dashboard")

# --- LOAD DATA ---
df_01 = conn.read(worksheet="2026_summary")

if not df_01.empty:
    st.subheader("Wager Summary by Team")
    st.bar_chart(data=df_01, x="Choice", y="Wager")
else:
    st.info("No data found to graph yet.")


st.divider()

# --- 2. LOGIN LOGIC  PRIVATE SESSION ---
if not st.user.get("is_logged_in"):
    st.subheader("📍 Place Your Bet")
    st.info("Log in to join the action!")
    # This creates the "Log in with Google" button
    if st.button("Log in with Google"):
        st.login("google")

else:
   st.write(f"Logged in as: **{st.user.email}**")
   if st.button("Log out"):
    st.logout()

    st.write(f"Logged in as: **{st.user.email}**")

    with st.form("betting_form"):
        choice = st.selectbox("Pick your team:", ["CSK", "MI"])
        amount = st.number_input("bet Amount (Zl)", min_value=5, step=1, max_value=10)
        submit = st.form_submit_button("Lock Bet 🔒")

        if submit:
            new_bet = pd.DataFrame([{"Email": st.user.email, "Choice": choice, "Wager": amount}])
            updated_df = pd.concat([df_01, new_bet], ignore_index=True)
            conn.update(worksheet="2026_summary", data=updated_df)

            st.balloons()
            st.success("Bet saved!")
            st.rerun()
