import pandas as pd
import streamlit as st
import time
from datetime import datetime
from utils.players import player_map
from utils.sheets_data import df_04,df_05, df_07



#df_07 = schedule of matches
#df_05 =  transactions log
#df_06 =



def match_bet(match_id, team1, team2, current_email, connection):
    # Passing the team & match id
    with st.form(key=f"form_{match_id}", clear_on_submit=True):
        st.subheader(f"🏏 upper.{team1} vs upper.{team2}")
        choice = st.radio("choose your side", [team1, team2], horizontal=True)
        amount = st.number_input(f"Bet Amount (Zl)", min_value=5, max_value=10, step=1)

        submit = st.form_submit_button("Lock Bet 🔒")

        if submit:
            new_row = pd.DataFrame([{
                "human_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "unix_time": int(time.time()),
                "email": current_email,
                "match_id": match_id,
                "choice": choice,
                "bet": amount,
                "player": player_map.get(current_email)
            }])

            updated_log = pd.concat([df_05, new_row], ignore_index=True)

            # 3. Push back to Google Sheets
            connection.update(worksheet="2026_bets_log", data=updated_log)
            st.balloons()
            time.sleep(1)
            st.rerun()


def betting_manager(current_email, df_07, df_05, connection):
    # check latest match & how many matches per day

    # 1. Get Today's Date in same format as Excel (adjust format if needed)
    today = pd.Timestamp.now().strftime("%Y-%m-%d")

    # 2. Filter for matches TODAY that don't have a result yet
    # We sort by match_time to get the early match first
    to_day = pd.Timestamp.now().strftime("%d-%m-%Y")

    upcoming = df_07[(df_07['match_date'] == to_day) &(df_07['result'].isna())].sort_values('match_time')

    if upcoming.empty:
        st.info(f"""
            **Code thinks today is:** `{to_day}`  
            **First date in Sheet is:** `{df_07['match_date'].iloc[0]}`  
            **Are they equal?** {to_day == str(df_07['match_date'].iloc[0])}
        """)
        st.info("📅 No matches scheduled for today!")
        return

    # 3. Create Columns for Match 1 and Match 2
    cols = st.columns(len(upcoming))

    for i, (_, match) in enumerate(upcoming.iterrows()):
        with cols[i]:
            match_bet(match['match_id'], match['team_1'], match['team_2'], current_email, df_05, connection)