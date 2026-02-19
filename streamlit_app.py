import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet="2026_summary")

st.dataframe(df)


# --- YOUR APP LOGIC ---
if st.user.get("is_logged_in"):
    st.write(f"Logged in as {st.user.email}")

    # Create a small form for the bet
    with st.form("betting_form"):
        choice = st.selectbox("Pick your winner:", ["Team Alpha", "Team Beta"])
        amount = st.number_input("Wager", min_value=1)
        submit = st.form_submit_button("Lock Bet 🔒")

        if submit:
            # 1. Get existing bets
            existing_data = conn.read(worksheet="2026_summary")

            # 2. Create the new row
            new_bet = pd.DataFrame([{
                "Email": st.user.email,
                "Choice": choice,
                "Wager": amount
            }])

            # 3. Add new bet to existing ones
            updated_df = pd.concat([existing_data, new_bet], ignore_index=True)

            # 4. Update the Google Sheet
            conn.update(worksheet="2026_summary", data=updated_df)

            st.balloons()
            st.success("Bet saved")
