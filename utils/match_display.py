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
    df_bets = conn.read(worksheet="2026_bets_raw", ttl=0)
    df_schedule = conn.read(worksheet="2026_schedule", ttl=0)
    return df_today, df_bets , df_schedule


@st.fragment(run_every=60)
def display_matches():

    df_today, df_bets , df_schedule = cached_bet_data()
    india_tz = pytz.timezone('Asia/Kolkata')
    current_time_str = datetime.now(india_tz).strftime("%H:%M")

    match_cols = ["today_01", "today_02"]

    for col in match_cols:
        val = df_today.iloc[0][col]

        if pd.notna(val) and str(val).strip().lower() != 'nil' :
            match_id = val
            bets_row = df_bets[df_bets.iloc[:, 0] == match_id]
            row_data = bets_row.squeeze()

            #for dead line extraction
            deadline_row = df_schedule[df_schedule['match_id'] == match_id]
            deadline_row_data = deadline_row.squeeze()
            deadline = str(deadline_row_data['match_time']).strip()
            if current_time_str > deadline:
                continue # skips it

            team_1:str = str(row_data['team_1']).strip().lower()
            team_2:str = str(row_data['team_2']).strip().lower()

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
    df_today, df_bets , df_schedule = cached_bet_data()
    conn = st.connection("gsheets", type=GSheetsConnection)
    india_tz = pytz.timezone('Asia/Kolkata')
    current_time_str = datetime.now(india_tz).strftime("%H:%M")

    # The columns in your Google Sheet that hold today's Match IDs
    match_cols = ["today_01", "today_02"]

    for col in match_cols:
        val = df_today.iloc[0][col]

        match_id = val

        # Skip if the cell is empty or 'nil'
        if pd.isna(match_id) or str(match_id).strip().lower() == 'nil':
            continue

        match_row = df_schedule[df_schedule['match_id'] == match_id]
        match_row_data = match_row.squeeze()
        deadline = str(match_row_data['match_time']).strip()


        bets_row = df_bets[df_bets['match_id'] == match_id]
        row_data = bets_row.squeeze()
        team_1 = str(row_data['team_1']).strip()
        team_2 = str(row_data['team_2']).strip()

        logo_1 = logos_map.get(team_1)
        logo_2 = logos_map.get(team_2)

        is_started = current_time_str >= deadline

        if not is_started:
            continue

        # 4. Filter Bet Logs for this Match
        match_bets = df_bets[df_bets['match_id'] == match_id]

        players = ['kalyan', 'subba', 'jaggu', 'balu', 'sravan', 'darsi']

        t1_list = []
        t2_list = []

        # 2. Loop through players to collect their choice and bet amount
        for p in players:
            # Get team choice and bet amount from the row
            choice = str(row_data.get(f'{p}_team', '')).strip().lower()
            amount = row_data.get(f'{p}_bet', 0)
            display_name = p.title()

            if choice == team_1.lower():
                t1_list.append(
                    f"<div style='color:#aaa; font-size:11px; margin-bottom:2px;'>👤 {display_name} ({amount}zł)</div>")
            elif choice == team_2.lower():
                t2_list.append(
                    f"<div style='color:#aaa; font-size:11px; margin-bottom:2px;'>👤 {display_name} ({amount}zł)</div>")

        # 3. Prepare Content based on Time
        if is_started:
            # REVEAL MODE: Join the pre-formatted list of strings
            t1_content = "".join(t1_list) if t1_list else "<div style='color:#444; font-size:10px;'>No Bets</div>"
            t2_content = "".join(t2_list) if t2_list else "<div style='color:#444; font-size:10px;'>No Bets</div>"
        else:
            # HIDDEN MODE: Just show the icons count
            t1_content = f"<div style='color:#ffcc00; font-size:22px;'>{'👤' * len(t1_list)}</div>"
            t2_content = f"<div style='color:#ffcc00; font-size:22px;'>{'👤' * len(t2_list)}</div>"

            # Fallback for hidden mode if 0 bets
            if not t1_list: t1_content = "<div style='color:#444; font-size:10px;'>No Bets</div>"
            if not t2_list: t2_content = "<div style='color:#444; font-size:10px;'>No Bets</div>"

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

