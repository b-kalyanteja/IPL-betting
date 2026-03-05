import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from utils.match_display import display_matches

# PREDICTION columns ()





# CREATE connection to Google sheets
conn = st.connection("gsheets", type=GSheetsConnection)



st.set_page_config(
    page_title="IPL 2026 Bets",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🏆 IPL'26 Bets")

st.divider()

st.write("Today's matches")

st.divider()
st.write("Player's Performance")

# Daily Cumilative graph


sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-m3xGBp4kDPQgG4-ZzockJy3E--gqPEFJGTtonfdfDX9Juuga0O0UPxTCUUPLmiNX_Op8kkEH0G_j/pubhtml?gid=642106326&single=true&widget=true&headers=false"

# Using Streamlit columns to center the content
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    st.markdown("##### 📅 Schedule & Points Table")
    components.html(f"""
        <div style="
            display: flex; 
            justify-content: center; 
            align-items: center; 
            width: 100%;
            border: 1px solid #333; 
            border-radius: 15px; 
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        ">
            <iframe src="{sheet_url}" 
                    width="100%" 
                    height="400" 
                    style="border: none;" 
                    scrolling="yes">
            </iframe>
        </div>
    """, height=420)


components.html(f"""
    <div style="width: 80%; overflow: hidden; border-radius: 15px; border: 1px solid #333;">
        <iframe src="{sheet_url}" 
                width="100%" 
                height="600" 
                style="border: none;" 
                scrolling="yes">
        </iframe>
    </div>
""", height=620)

display_matches()



