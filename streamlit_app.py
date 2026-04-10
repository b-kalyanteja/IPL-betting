import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from utils.match_display import display_matches
from utils.cumilative_graph import performance_graph, current_status, committee_status
from utils.prediction_daily import today_prediction
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

@st.dialog("super cena 🛍️")
def show_ad():
    # GIF linked to temp.com
    st.write(
        '<a href="https://temu.com" target="_blank">'
        '<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExamFmbmtwMnN2MXY5bGZrZ2IycGExOHY0djNvanF1Z3c4MGtkNjR6MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/c9MRRmDxtnlMZMN5Ye/giphy.gif" style="width:100%;">'
        '</a>',
        unsafe_allow_html=True
    )

show_ad()

display_match_afterstart()
display_matches()
st.divider()

today_prediction()
st.divider()

st.write("Player's Performance")
performance_graph()
st.divider()


current_status()
st.divider()

committee_status()
st.divider()



def scoreboard():

    html_code = """
    <div id="scoreboard-widget" style="width: 100%; overflow: hidden;">
        <script src="https://cdorgapi.b-cdn.net/widgets/score.js"></script>
    </div>
    <style>
        /* Hide scrollbars within the iframe body */
        body { 
            margin: 0; 
            padding: 0; 
            overflow: hidden; 
            background-color: transparent; 
        }
    </style>
    """

    components.html(html_code, height=200, scrolling=False)
scoreboard()