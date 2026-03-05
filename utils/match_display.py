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
    <div style="background-color:#000; border:1px solid #333; border-radius:15px; padding:15px; width:100%;">
    <table style="width:100%; border-collapse:collapse; text-align:center; table-layout:fixed;">
      <tr>
        <td style="width:40%; vertical-align:middle;">
          <img src="{logo_1}" style="width:50px; height:50px; border-radius:50%; background:#fff; padding:3px;">
          <div style="color:#fff; font-weight:bold; font-size:14px; margin-top:5px;">{team_1.upper()}</div>
          <div style="font-size:14px;">{t1_icons}</div>
        </td>
        <td style="width:20%; vertical-align:middle; color:#888; font-weight:bold; font-size:18px;">
          VS
        </td>
        <td style="width:40%; vertical-align:middle;">
          <img src="{logo_2}" style="width:50px; height:50px; border-radius:50%; background:#fff; padding:3px;">
          <div style="color:#fff; font-weight:bold; font-size:14px; margin-top:5px;">{team_2.upper()}</div>
          <div style="font-size:14px;">{t2_icons}</div>
        </td>
      </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.divider()


@st.cache_data(ttl=5)
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

            st.write(all_bets)
            t1_bets: int = all_bets.count(team_1)
            st.write(t1_bets)
            t2_bets: int = all_bets.count(team_2)
            st.write(t2_bets)

            match_widget(team_1=team_1, team_2=team_2, t1_bets=t1_bets, t2_bets=t2_bets)
        else:
            continue
