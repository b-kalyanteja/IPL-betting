import streamlit as st
import pandas as pd
from streamlit import cache_data
from utils.logos import logos_map
from streamlit_gsheets import GSheetsConnection
import pytz
from datetime import datetime

def match_widget(team_1, team_2, t1_bets,t2_bets):

    logo_1 = logos_map.get(team_1)
    logo_2 = logos_map.get(team_2)

    t1_icons = ("👤" * t1_bets)
    t2_icons = ("👤" * t2_bets)

    # Copy and Paste this exactly - DO NOT INDENT THE HTML LINES
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e1e1e 0%, #000000 100%); border: 1px solid #333; border-radius: 20px; padding: 20px; width: 100%; box-shadow: 0 10px 20px rgba(0,0,0,0.5); margin: 10px 0;">
    <table style="width:100%; border-collapse:collapse; text-align:center; table-layout:fixed; border:none;">
    <tr style="border:none;">
    <td style="width:40%; vertical-align:middle; border:none;">
    <div style="display: flex; flex-direction: column; align-items: center;">
    <img src="{logo_1}" style="width:65px; height:65px; border-radius:50%; background:#fff; padding:4px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); object-fit:contain;">
    <div style="color:#fff; font-weight:900; font-size:16px; margin-top:10px; letter-spacing:1px;">{team_1.upper()}</div>
    <div style="margin-top:5px;">{t1_icons}</div>
    </div>
    </td>
    <td style="width:20%; vertical-align:middle; border:none;">
    <div style="color:#555; font-weight:bold; font-size:18px; position:relative;">
    <span style="background:#111; padding:5px 10px; border-radius:10px; border:1px solid #333;">VS</span>
    </div>
    </td>
    <td style="width:40%; vertical-align:middle; border:none;">
    <div style="display: flex; flex-direction: column; align-items: center;">
    <img src="{logo_2}" style="width:65px; height:65px; border-radius:50%; background:#fff; padding:4px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); object-fit:contain;">
    <div style="color:#fff; font-weight:900; font-size:16px; margin-top:10px; letter-spacing:1px;">{team_2.upper()}</div>
    <div style="margin-top:5px;">{t2_icons}</div>
    </div>
    </td>
    </tr>
    </table>
    </div>
    """, unsafe_allow_html=True)


#have to cache as the API have limits
@st.cache_data(ttl=10)
def cached_bet_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_today = conn.read(worksheet="2026_today", ttl=0)
    df_schedule = conn.read(worksheet="2026_bets_raw", ttl=0)
    return df_today, df_schedule


@st.fragment(run_every=60)
def display_matches():

    df_today, df_schedule = cached_bet_data()
    india_tz = pytz.timezone('Asia/Kolkata')
    current_time_str = datetime.now(india_tz).strftime("%H:%M")

    match_cols = ["today_01", "today_02"]

    for col in match_cols:
        val = df_today.iloc[0][col]

        if pd.notna(val) and str(val).strip().lower() != 'nil' :
            match_id = val
            schedule_row = df_schedule[df_schedule.iloc[:, 0] == match_id]

            row_data = schedule_row.squeeze()
            deadline = str(row_data['match_time']).strip()
            if current_time_str > deadline:
                continue # skips it

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


def display_match_afterstart():
    # 1. Fetch all data
    df_today, df_schedule = cached_bet_data()
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_logs = connection.read(worksheet="2026_bets_raw", ttl=0)

    india_tz = pytz.timezone('Asia/Kolkata')
    current_time_str = datetime.now(india_tz).strftime("%H:%M")

    # The columns in your Google Sheet that hold today's Match IDs
    match_cols = ["today_01", "today_02"]

    for col in match_cols:
        match_id = df_today.iloc[0].get(col)

        # Skip if the cell is empty or 'nil'
        if pd.isna(match_id) or str(match_id).strip().lower() == 'nil':
            continue

        # 2. Extract Match Details from Schedule
        schedule_row = df_schedule[df_schedule.iloc[:, 0] == match_id]
        if schedule_row.empty:
            continue

        row_data = schedule_row.squeeze()
        team_1 = str(row_data['t1']).strip()
        team_2 = str(row_data['t2']).strip()
        deadline = str(row_data['match_time']).strip()
        logo_1 = row_data.get('logo1', '')
        logo_2 = row_data.get('logo2', '')

        # 3. Time Logic
        is_started = current_time_str >= deadline

        # 4. Filter Bet Logs for this Match
        match_bets = df_logs[df_logs['match_id'] == match_id]
        t1_voters = match_bets[match_bets['choice'].str.strip().lower() == team_1.lower()]
        t2_voters = match_bets[match_bets['choice'].str.strip().lower() == team_2.lower()]

        # 5. Prepare Content based on Time
        if is_started:
            t1_content = "".join(
                [f"<div style='color:#aaa; font-size:11px;'>{r['player']} ({r['bet']}zł)</div>" for _, r in
                 t1_voters.iterrows()])
            t2_content = "".join(
                [f"<div style='color:#aaa; font-size:11px;'>{r['player']} ({r['bet']}zł)</div>" for _, r in
                 t2_voters.iterrows()])
        else:
            # Mask names until match starts - just show icons
            t1_content = f"<div style='color:#ffcc00; font-size:18px;'>{'👤' * len(t1_voters)}</div>"
            t2_content = f"<div style='color:#ffcc00; font-size:18px;'>{'👤' * len(t2_voters)}</div>"

        if not t1_content: t1_content = "<div style='color:#444; font-size:10px;'>No Bets</div>"
        if not t2_content: t2_content = "<div style='color:#444; font-size:10px;'>No Bets</div>"

        # 6. Render the HTML Card (Ensure zero indentation on the triple quotes)
        st.markdown(f"""
<div style="background: linear-gradient(135deg, #1e1e1e 0%, #000000 100%); border: 1px solid #333; border-radius: 20px; padding: 20px; width: 100%; box-shadow: 0 10px 20px rgba(0,0,0,0.5); margin: 10px 0;">
<table style="width:100%; border-collapse:collapse; text-align:center; table-layout:fixed; border:none;">
<tr style="border:none;">
<td style="width:40%; vertical-align:middle; border:none;">
<div style="display: flex; flex-direction: column; align-items: center;">
<img src="{logo_1}" style="width:65px; height:65px; border-radius:50%; background:#fff; padding:4px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); object-fit:contain;">
<div style="color:#fff; font-weight:900; font-size:16px; margin-top:10px; letter-spacing:1px;">{team_1.upper()}</div>
<div style="margin-top:5px;">{t1_content}</div>
</div>
</td>
<td style="width:20%; vertical-align:middle; border:none;">
<div style="color:#555; font-weight:bold; font-size:18px; position:relative;">
<span style="background:#111; padding:5px 10px; border-radius:10px; border:1px solid #333;">VS</span>
</div>
</td>
<td style="width:40%; vertical-align:middle; border:none;">
<div style="display: flex; flex-direction: column; align-items: center;">
<img src="{logo_2}" style="width:65px; height:65px; border-radius:50%; background:#fff; padding:4px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); object-fit:contain;">
<div style="color:#fff; font-weight:900; font-size:16px; margin-top:10px; letter-spacing:1px;">{team_2.upper()}</div>
<div style="margin-top:5px;">{t2_content}</div>
</div>
</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)

