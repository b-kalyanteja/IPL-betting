import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit_gsheets import GSheetsConnection

from utils.match_display import cached_bet_data

# TODO
'''
JAgadeesh to write code for the predictor :

if predictor logs in and select a match the nit's finalized ... He cannot change it 
He has to give prediction on or before predictor's deadline, his prediction will b upodated against match_id in the 2026_bets_raw sheets

write predictor's log in code also 
'''



# ON MAIN PAGE  : Prediction Status
@st.cache_data(ttl=30)
def today_prediction():

    conn = st.connection("gsheets", type=GSheetsConnection)
    df_09= conn.read(worksheet="2026_today_prediction", ttl=0)

    cols = ["today_01", "today_02"]

    raw_vals = df_09[cols].iloc[0].tolist()

    # 2. Keep only values that are NOT empty (removes NaN and None)
    teams = [str(t) for t in raw_vals if pd.notna(t)]

    if len(teams) == 2:
        title = "Genie's Double Pick"
        content = f"<b>{teams[0].upper()}</b> <span style='color:#555;'>|</span> <b>{teams[1]}</b>"
    elif len(teams) == 1:
        title = "Genie's Top Pick"
        content = f"<b>{teams[0].upper()}</b>"
    else:
        title = "Genie is Resting"
        content = "Predictions coming soon... 😴"

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