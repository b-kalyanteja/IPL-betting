import streamlit as st
from utils.logos import logos_map

def match_widget(team_1, team_2, t1_bets,t2_bets):

    logo_1 = logos_map.get(team_1)
    logo_2 = logos_map.get(team_2)

    team_1_name = team_1.upper()
    team_2_name = team_2.upper()

    # CSS Styling
    st.markdown("""
        <style>
        .match-container {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #333;
            margin-bottom: 20px;
        }
        .team-box { text-align: center; width: 120px; }
        .team-logo { width: 80px; height: 80px; object-fit: contain; border-radius: 50%; background: #fff; padding: 5px; }
        .vs-divider {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            padding: 0 20px;
        }
        .line {
            height: 2px;
            width: 100%;
            background: linear-gradient(90deg, #00FF00, #FF0000);
            margin: 10px 0;
        }
        .bet-icons { font-size: 20px; color: #aaa; }
        .vs-text { font-weight: bold; color: #888; font-size: 1.2rem; }
        </style>
    """, unsafe_allow_html=True)


    t1_icons = ("👤" * t1_bets)
    t2_icons = ("👤" * t2_bets)

    # Build the Widget
    st.markdown(f"""
    <div class="match-container">
        <div class="team-box">
            <img src="{logo_1}" class="team-logo">
            <br><strong>{team_1_name}</strong>
            <div class="bet-icons">{t1_icons}</div>
        </div>
               
        <div class="team-box">
            <img src="{logo_2}" class="team-logo">
            <br><strong>{team_2_name}</strong>
            <div class="bet-icons">{t2_icons}</div>
        </div>              
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="match-container">
        <div class="team-box">
            <img src="{logo_2}" class="team-logo">
            <br><strong>{team_2_name}</strong>
            <div class="bet-icons">{t2_icons}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- EXAMPLE USAGE ---
st.title("Today's Featured Match")

