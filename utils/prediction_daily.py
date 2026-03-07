import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import time
from streamlit_gsheets import GSheetsConnection

from utils.match_display import cached_bet_data

#@st.cache_data(ttl=1)
# def prediction_next_match():
#     conn = st.connection("gsheets", type=GSheetsConnection)
#     df_log = conn.read(worksheet="2026_bets_log", ttl=0)
#     df_nxt = conn.read(worksheet="2026_next_match", ttl=0)
#     df_bets = conn.read(worksheet="2026_bets_raw", ttl=0)
#
#     conn = st.connection("gsheets", type=GSheetsConnection)
#
#     row = df_today.iloc[0]
#
#
#     # 3. Check if there is anything to predict
#     if not match_ids:
#         st.info("🛋️ Nothing to predict today... Take rest!")
#         return
#         st.stop()
#
#     st.subheader("Predictions Poll")
#
#         match_row = df_bets[df_bets['match_id'] == m_id]
#
#         if match_row.empty:
#             st.error(f"Match ID `{m_id}` not found in bets sheet.")
#             continue
#
#         row_index = match_row.index[0]
#         t1 = str(match_row.at[row_index, 'team_1']).strip()
#         t2 = str(match_row.at[row_index, 'team_2']).strip()
#
#         # Check if prediction already exists in the row
#         current_pred = match_row.at[row_index, 'prediction'] if 'prediction' in df_bets.columns else None
#
#         # Display the UI
#         st.write(f"**Match: {t1.upper()} vs {t2.upper()}**")
#
#         if not pd.isna(current_pred) and str(current_pred).strip() != "":
#             st.success(f"Locked Prediction: **{str(current_pred).upper()}**")
#             continue  # Move to next match if already predicted
#
#         # Form for prediction
#         with st.form(key=f"poll_{m_id}"):
#             choice = st.radio("Who will win?", [t1, t2], horizontal=True, key=f"radio_{m_id}")
#             submit = st.form_submit_button("Submit Prediction 🚀")
#
#             if submit:
#                 # A. Update the Raw Sheet (Horizontal)
#                 if 'prediction' not in df_bets.columns:
#                     df_bets['prediction'] = ""
#
#                 df_bets.at[row_index, 'prediction'] = choice
#                 conn.update(worksheet="2026_bets_raw", data=df_bets)
#
#                 # B. Save a copy to the Log Sheet
#                 new_log = pd.DataFrame([{
#                     "human_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                     "match_id": m_id,
#                     "type": "POLL_PREDICTION",
#                     "choice": choice,
#                     "user": st.session_state.get('user_email', 'admin')  # Adjust based on your login
#                 }])
#
#                 updated_log = pd.concat([df_log, new_log], ignore_index=True)
#                 conn.update(worksheet="2026_bets_log", data=updated_log)
#
#                 st.toast(f"Prediction for {m_id} saved!")
#                 st.cache_data.clear()
#                 time.sleep(1)
#                 st.rerun()




# ON MAIN PAGE  : Prediction Status
@st.cache_data(ttl=30)
def today_prediction():

    conn = st.connection("gsheets", type=GSheetsConnection)
    df_09= conn.read(worksheet="2026_today_prediction", ttl=0)

    cols = ["today_01", "today_02"]

    raw_vals = df_09[cols].iloc[0].tolist()

    # 2. Keep only values that are NOT empty (removes NaN and None)
    teams = [str(t) for t in raw_vals if pd.notna(t)and str(t).lower() != "nil"]

    if len(teams) == 2:
        title = "Predictor's Double Dhamaaka"
        content = f"<b>{teams[0].upper()}</b> <span style='color:#555;'>➕</span> <b>{teams[1].upper()}</b>"
    elif len(teams) == 1:
        title = "Predictor's Pick "
        content = f"<b>{teams[0].upper()}</b>"
    else:
        title = "Predictor is Sleeping 😴"
        content = "Please Wait coming soon... "

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
                <div style="color: #00FFCC; font-size: 15px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px; opacity: 0.8;">
                    {title} 🧞‍♂️
                </div>
                <div style="color: Black; font-size: 20px; font-weight: 700; letter-spacing: 0.5px;">
                    {content} <span style="font-style: normal; margin-left: 5px;">✌🏼</span>
                </div>
            </div>
        """, unsafe_allow_html=True)