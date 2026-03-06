import streamlit as st
import pandas as pd
import time
from datetime import datetime
from typing import Optional
from streamlit_gsheets import GSheetsConnection


def _is_blank(value) -> bool:
    if pd.isna(value):
        return True
    return str(value).strip().lower() in {"", "none", "nan", "nil"}


def _first_existing_column(df: pd.DataFrame, candidates) -> Optional[str]:
    for col in candidates:
        if col in df.columns:
            return col
    return None

def prediction_next_match():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_bets = conn.read(worksheet="2026_bets_raw", ttl=0)
    df_nxt = conn.read(worksheet="2026_next_match", ttl=0)

    if df_nxt.empty:
        st.info("No next match configured in `2026_next_match`.")
        return

    if df_bets.empty:
        st.info("`2026_bets_raw` is empty, cannot lock prediction right now.")
        return

    next_id_col = _first_existing_column(df_nxt, ["next_match", "next_match_id", "match_id", "id"])
    next_match_id = df_nxt.iloc[0][next_id_col] if next_id_col else df_nxt.iloc[0, 0]

    if _is_blank(next_match_id):
        st.warning("Next match value is empty in `2026_next_match`.")
        return

    bets_match_col = _first_existing_column(df_bets, ["match_id", "id"])
    if bets_match_col:
        match_mask = (
            df_bets[bets_match_col].astype(str).str.strip().str.lower()
            == str(next_match_id).strip().lower()
        )
    else:
        match_mask = (
            df_bets.iloc[:, 0].astype(str).str.strip().str.lower()
            == str(next_match_id).strip().lower()
        )

    if not match_mask.any():
        st.error(f"Next match `{next_match_id}` not found in `2026_bets_raw`.")
        return

    row_index = df_bets.index[match_mask][0]
    team_1_col = _first_existing_column(df_bets, ["t1", "team_1", "team1"])
    team_2_col = _first_existing_column(df_bets, ["t2", "team_2", "team2"])

    if not team_1_col or not team_2_col:
        st.error("Could not find team columns (`t1`/`t2`) in `2026_bets_raw`.")
        return

    team_1 = str(df_bets.at[row_index, team_1_col]).strip()
    team_2 = str(df_bets.at[row_index, team_2_col]).strip()

    prediction_col = _first_existing_column(
        df_bets,
        ["predictor", "predictor_pick", "predictor_choice", "prediction", "poll"],
    )

    if prediction_col is None:
        prediction_col = "predictor_choice"
        df_bets[prediction_col] = ""

    current_pick = df_bets.at[row_index, prediction_col]

    st.subheader(f"Next Match: {team_1.upper()} vs {team_2.upper()}")
    st.caption(f"Match ID: {next_match_id}")

    if not _is_blank(current_pick):
        st.success(f"Locked prediction: {str(current_pick).upper()}")
        st.info("Prediction already submitted. You cannot change it.")
        return

    with st.form(key=f"predictor_next_match_{next_match_id}", clear_on_submit=False):
        choice = st.radio(
            "Choose winner",
            [team_1, team_2],
            horizontal=True,
            format_func=lambda x: str(x).upper(),
        )
        submit = st.form_submit_button("Lock Prediction 🔒")

    if submit:
        df_bets.at[row_index, prediction_col] = choice

        # Fill optional audit columns only when they already exist in the sheet.
        optional_updates = {
            "predictor_email": st.user.get("email", ""),
            "predictor_unix_time": int(time.time()),
            "predictor_human_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        for col, value in optional_updates.items():
            if col in df_bets.columns:
                df_bets.at[row_index, col] = value

        conn.update(worksheet="2026_bets_raw", data=df_bets)
        st.cache_data.clear()
        st.success(f"Prediction locked for match `{next_match_id}`: {choice.upper()}")
        time.sleep(0.8)
        st.rerun()


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
        title = "Predictor's Double Dhamaaka"
        content = f"<b>{teams[0].upper()}</b> <span style='color:#555;'>➕</span> <b>{teams[1].upper()}</b>"
    elif len(teams) == 1:
        title = "Predictor's Pick "
        content = f"<b>{teams[0].upper()}</b>"
    else:
        title = "Predictor is Sleeping 😴"
        content = "Predictions coming soon... "

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