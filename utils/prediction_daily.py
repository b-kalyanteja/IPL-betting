import pytz
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import time
from streamlit_gsheets import GSheetsConnection
from utils.players import logos_map

from utils.match_display import cached_bet_data
@st.cache_data(ttl=20)
def get_all_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_log = conn.read(worksheet="2026_bets_log", ttl=10)
        df_nxt = conn.read(worksheet="2026_next_match", ttl=10)
        df_bets = conn.read(worksheet="2026_bets_raw", ttl=10)
        df_schedule = conn.read(worksheet="2026_schedule", ttl=10)
        return df_log, df_nxt, df_bets, df_schedule
    except Exception as e:
        st.error("📉 Database server -API Free Limit or wait 30 seconds")
        if st.button("Try Again 🔄"):
            st.rerun()
        st.stop()

def prediction_next_match(current_email):

    df_log, df_nxt, df_bets, df_schedule = get_all_data()
    conn = st.connection("gsheets", type=GSheetsConnection)

    india_tz = pytz.timezone('Asia/Kolkata')
    now_india = datetime.now(india_tz)
    current_time_str = now_india.strftime("%H:%M")


    nxt_match_id = df_nxt['next_match'].iloc[0]

    if  nxt_match_id == 'nil' :
        st.write (" No Matches For today.. Go Sleep 😴")
        st.stop()

    already_predicted = df_log[(df_log['email'] == current_email) & (df_log['match_id'] == nxt_match_id)]
    if not already_predicted.empty:
        st.info(f"✅ You have already Predicted .. He He He Hu Hu Hu")
        st.stop()

    else :
        match_row = df_schedule[df_schedule['match_id'] == nxt_match_id]
        deadline_time = str(match_row['pred_deadline'].iloc[0])
        team_1 = str(match_row['team_1'].iloc[0]).strip()
        team_2 = str(match_row['team_2'].iloc[0]).strip()
        prediction = match_row['prediction'].fillna("empty").iloc[0]


        if ( current_time_str > deadline_time) :
            st.subheader(f"🏏 {team_1.upper()} vs {team_2.upper()}")
            st.error(f"OOPS ⌛️ TIME UP! Betting closed (Deadline: {deadline_time} IST)")
            if prediction == 'empty':
                st.write(f"OOPS you forgot to predict too 🤷🏻‍♂️")
            else:
                st.write(f"Your Victory Prediction :**{prediction.upper()}**")
            st.stop()

        else :
            with st.form(key=f"form_{nxt_match_id}", clear_on_submit=True):
                st.subheader(f"🏏 {team_1.upper()} vs {team_2.upper()}")

                choice = st.radio("Choose your side", [team_1, team_2], horizontal=True)
                choice_lower = choice.lower()

                st.caption(f"🕒 Deadline today at {deadline_time} IST")

                submit = st.form_submit_button("Confirm Bet 🔒")

                if submit:
                    st.session_state[f"submitting_{nxt_match_id}"] = True

                    # time re-check
                    now_india = datetime.now(india_tz).strftime("%H:%M")
                    if now_india > deadline_time:
                        st.error("Just Miss !!! dead line crossed Macha")
                        st.rerun()
                    else:
                        # Add bet to log
                        new_row = pd.DataFrame([{
                            "human_time": datetime.now(india_tz).strftime("%Y-%m-%d %H:%M:%S"),
                            "unix_time": int(time.time()),
                            "email": current_email,
                            "match_id": nxt_match_id,
                            "choice": choice_lower,
                            "bet": 0,
                            "player": "predictor",
                            "agent": st.context.headers.get("User-Agent")
                        }])

                        updated_log = pd.concat([df_log, new_row], ignore_index=True)
                        conn.update(worksheet="2026_bets_log", data=updated_log)


                        st.toast(f"Good luck on {choice}!", icon="🤞")
                        time.sleep(1)
                        st.balloons()
                        time.sleep(2)
                        st.session_state[f"submitting_{nxt_match_id}"] = False
                        st.cache_data.clear()
                    st.stop()



# ON MAIN PAGE  : Prediction Status
@st.cache_data(ttl=10)
def today_prediction():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_09= conn.read(worksheet="2026_today_prediction", ttl=10)
    except Exception as e:
        st.error("📉 Database server -API Free Limit or wait 30 seconds")
        if st.button("Try Again 🔄"):
            st.rerun()
        st.stop()

    cols = ["today_01", "today_02"]

    raw_vals = df_09[cols].iloc[0].tolist()

    # 2. Keep only values that are NOT empty (removes NaN and None)
    teams: list = [str(t).strip() for t in raw_vals if pd.notna(t) and str(t).lower() != "nil"]

    logo_size = "40px"
    st.write(teams)
    st.write(teams[1])


    if len(teams) == 2:
        title = "Predictor's Double Dhamaaka"

        logo_1 = logos_map.get(teams[0].lower(), logos_map['ipl'])
        logo_2 = logos_map.get(teams[1].lower(), logos_map['ipl'])

        content = f"""
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <img src="{logo_1}" width="{logo_size}">
                    <span style='color:#555; font-size: 25px;'>+</span>
                    <img src="{logo_2}" width="{logo_size}">
                </div>
            """

        # CASE: One Team (Predictor's Pick)
    elif len(teams) == 1:
        title = "Predictor's Pick"
        logo_1 = logos_map.get(teams[0].lower(), logos_map['ipl'])

        content = f"""
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <img src="{logo_1}" width="{logo_size}">
                </div>"""

        # CASE: No Teams
    else:
        title = "Predictor on power nap 😴"
        content = "Please be Patient"

    st.markdown(f"""
                <div style="
                    background: rgba(0, 255, 204, 0.05);
                    border: 1px solid rgba(0, 255, 204, 0.2);
                    border-radius: 15px;
                    padding: 15px;
                    text-align: center;
                    margin: 10px 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                ">
                    <div style="color: #FF6B6B; font-size: 15px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px; opacity: 0.8;">
                        {title} 🧞‍♂️
                    </div>
                    <div style="color: #333333; font-size: 22px; font-weight: 700; letter-spacing: 0.5px;">
                        {content}
                    </div>
                </div>
            """, unsafe_allow_html=True)