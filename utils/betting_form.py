import pandas as pd
import streamlit as st
import time
from datetime import datetime
from utils.players import player_map
from streamlit_gsheets import GSheetsConnection
import pytz
import random

@st.cache_data(ttl=1)
def clock_bar():
    india_tz = pytz.timezone('Asia/Kolkata')
    ist_now = datetime.now(india_tz).strftime("%H:%M:%S")
    #st.markdown("### 🕒 Indian Time : ")
    st.title(f"🕒 Indian Time : {ist_now}")




def match_bet(match_id, team_1, team_2, current_email, dead_line, match_type, connection):
    # 1. Check if we are currently "in progress"
    if f"submitting_{match_id}" not in st.session_state:
        st.session_state[f"submitting_{match_id}"] = False

    with st.form(key=f"form_{match_id}", clear_on_submit=True):
        st.subheader(f"🏏 {team_1.upper()} vs {team_2.upper()}")

        # Determine limits based on match type
        bet_min, bet_max = 5, 10
        if match_type.lower() == "semis":
            bet_min, bet_max = 8, 12
        elif match_type.lower() == "final":
            bet_min, bet_max = 15, 20

        choice = st.radio("choose your side", [team_1, team_2], horizontal=True)
        amount = st.number_input("Bet Amount (zł)", bet_min, bet_max, step=1)

        st.caption(f"🕒 today at {dead_line.lower()} ist")

        # 2. Disable button if already clicked
        submit = st.form_submit_button("Confirm Bet 🔒", disabled=st.session_state[f"submitting_{match_id}"])

        if submit:
            st.session_state[f"submitting_{match_id}"] = True

            india_tz = pytz.timezone('Asia/Kolkata')
            now_india = datetime.now(india_tz)

            try:

                deadline_hour, deadline_minute = map(int, dead_line.split(':'))
                deadline_time_obj = datetime.strptime(f"{deadline_hour}:{deadline_minute}", "%H:%M").time()

                # Compare it with the current time
                if now_india.time() > deadline_time_obj:
                    st.error("🚫 TIME UP! The betting deadline has passed.")
                    st.toast("Too late!", icon="⏰")
                    st.session_state[f"submitting_{match_id}"] = False
                    st.rerun()  # Use rerun instead of stop for a cleaner refresh
                    return

            except ValueError:
                st.error("Internal error: Invalid deadline format.")
                st.session_state[f"submitting_{match_id}"] = False
                st.rerun()
                return

            else:
                with st.spinner("Locking your bet..."):
                    new_row = pd.DataFrame([{
                        "human_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "unix_time": int(time.time()),
                        "email": current_email,
                        "match_id": match_id,
                        "choice": choice,
                        "bet": amount,
                        "player": player_map.get(current_email),
                        "agent": st.context.headers.get("User-Agent")
                    }])

                    # Fetch and Update
                    fresh_df_05 = connection.read(worksheet="2026_bets_log")
                    updated_log = pd.concat([fresh_df_05, new_row], ignore_index=True)
                    connection.update(worksheet="2026_bets_log", data=updated_log)

                # Success Feedback
                st.toast("Bet Submitted. Good Luck!", icon="🤞")
                random.choice([st.snow, st.balloons])()
                time.sleep(2)

                st.cache_data.clear()

                # Reset submission flag and refresh
                st.session_state[f"submitting_{match_id}"] = False
                st.rerun()


def betting_manager(current_email):
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = pd.Timestamp.now(tz=ist)

    current_day = now_ist.day  # e.g., 6
    current_month = now_ist.month

    conn = st.connection("gsheets", type=GSheetsConnection)
    df_07 = conn.read(worksheet="2026_schedule", ttl=1)

    df_07['date'] = pd.to_numeric(df_07['date'], errors='coerce')
    df_07['month'] = pd.to_numeric(df_07['month'], errors='coerce')

    #prod formula for upcoming
    upcoming = df_07[(df_07['date'] == current_day) & (df_07['month'] == current_month) &(df_07['result'].isna())].sort_values('match_time')
    #st.dataframe(upcoming)


    if upcoming.empty:
        st.info("📅 No matches scheduled for today!")
        return

    # 3. Create Columns for Match 1 and Match 2
    cols = st.columns(len(upcoming))

    for i, (_, match) in enumerate(upcoming.iterrows()):
        with cols[i]:
            match_bet(match_id=match['match_id'],team_1= match['team_1'],team_2= match['team_2'],current_email= current_email, dead_line = match['bet_deadline'], match_type= match['match_type'], connection= conn)