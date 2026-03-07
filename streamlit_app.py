import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from utils.match_display import display_matches
from utils.cumilative_graph import performance_graph, current_status
#from utils.prediction_daily import today_prediction
from utils.match_display import  display_match_afterstart
import plotly.express as px


# CREATE connection to Google sheets
conn = st.connection("gsheets", type=GSheetsConnection)



st.set_page_config(
    page_title="IPL 2026 Bets",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🏆 IPL'26 Bets")

display_match_afterstart()
display_matches()
st.divider()

# today_prediction()
st.divider()

st.write("Player's Performance")
performance_graph()
st.divider()


current_status()
st.divider()





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


