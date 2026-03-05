import streamlit as st
from utils.logos import logos_map

def match_widget(team_1, team_2, t1_bets,t2_bets):

    logo_1 = logos_map.get(team_1)
    logo_2 = logos_map.get(team_2)

    team_1_name = team_1.upper()
    team_2_name = team_2.upper()

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
