import streamlit as st
import pandas as pd
from streamlit import cache_data

from utils.logos import logos_map
from streamlit_gsheets import GSheetsConnection

def match_widget(team_1, team_2, t1_bets,t2_bets):

    logo_1 = logos_map.get(team_1)
    logo_2 = logos_map.get(team_2)

    t1_icons = ("👤" * t1_bets)
    t2_icons = ("👤" * t2_bets)

    st.markdown(f"""
    <style>
        .match-card {{
            /* This creates the contrast: light tint in dark mode, dark tint in light mode */
            background-color: rgba(128, 128, 128, 0.1); 
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 20px;
            padding: 20px;
            width: 100%;
            /* Add a subtle glow/shadow to lift it off the page */
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            backdrop-filter: blur(5px);
        }}

        .team-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        .team-name {{
            color: var(--text-color);
            font-weight: 800;
            font-size: clamp(13px, 4vw, 18px);
            margin-top: 10px;
            letter-spacing: 0.5px;
        }}

        .vs-circle {{
            background: var(--background-color);
            border: 1px solid var(--divider-color);
            color: var(--secondary-text-color);
            width: 40px;
            height: 40px;
            line-height: 40px;
            border-radius: 50%;
            font-weight: bold;
            font-size: 14px;
            display: inline-block;
        }}
    </style>

    <div class="match-card">
    <table style="width:100%; border-collapse:collapse; text-align:center; table-layout:fixed;">
      <tr>
        <td style="width:40%; vertical-align:middle;">
          <div class="team-container">
            <img src="{logo_1}" style="width:75%; max-width:90px; aspect-ratio:1/1; border-radius:50%; background: white; padding:4px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
            <div class="team-name">{team_1.upper()}</div>
            <div style="font-size:12px; opacity: 0.8;">{t1_icons}</div>
          </div>
        </td>

        <td style="width:20%; vertical-align:middle;">
          <div class="vs-circle">VS</div>
        </td>

        <td style="width:40%; vertical-align:middle;">
          <div class="team-container">
            <img src="{logo_2}" style="width:75%; max-width:90px; aspect-ratio:1/1; border-radius:50%; background: white; padding:4px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
            <div class="team-name">{team_2.upper()}</div>
            <div style="font-size:12px; opacity: 0.8;">{t2_icons}</div>
          </div>
        </td>
      </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)
    st.divider()


@st.cache_data(ttl=10)
def cached_bet_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_today = conn.read(worksheet="2026_today", ttl=0)
    df_schedule = conn.read(worksheet="2026_bets_raw", ttl=0)
    return df_today, df_schedule



def display_matches():

    df_today, df_schedule = cached_bet_data()

    match_cols = ["today_01", "today_02"]

    for col in match_cols:
        val = df_today.iloc[0][col]

        if pd.notna(val) and str(val).strip().lower() != 'nil' :

            match_id = val
            schedule_row = df_schedule[df_schedule.iloc[:, 0] == match_id]

            row_data = schedule_row.squeeze()
            team_1:str = str(row_data['t1']).strip().lower()
            team_2:str = str(row_data['t2']).strip().lower()

            bet_cols = ['kalyan_team','jaggu_team','subba_team','balu_team','sravan_team','darsi_team']
            bet_rows = row_data.loc[bet_cols]
            all_bets = [str(val).strip().lower() for val in bet_rows.tolist()]

            #st.write(all_bets)
            t1_bets: int = all_bets.count(team_1)
            #st.write(t1_bets)
            t2_bets: int = all_bets.count(team_2)
            #st.write(t2_bets)

            match_widget(team_1=team_1, team_2=team_2, t1_bets=t1_bets, t2_bets=t2_bets)
        else:
            continue
