import streamlit as st
from pathlib import Path
from streamlit_gsheets import GSheetsConnection

@st.cache_data(ttl=30)
def predictor_stats():

    conn = st.connection("gsheets", type=GSheetsConnection)
    df_04 = conn.read(worksheet="2026_bets_raw", ttl=0)

    prediction_results = [
        str(x).strip().lower()
        for x in df_04.iloc[0:77, 7].tolist()
        if str(x).strip().lower() in ['w', 'l', 'd']
    ]

    values_2026 = "".join(
        ["🟢" if x == 'w' else "🦜" if x == 'l' else "⚠️" for x in prediction_results if x in ['w', 'l', 'd']])

    ttl_w = prediction_results.count('w')
    ttl_a: int = len(prediction_results)
    percent_ = ((ttl_w /ttl_a) * 100) if ttl_a > 0 else 0
    percent_2026 = f"{percent_:.1f}%"

    return values_2026, percent_2026

@st.cache_data(ttl=30)
def hall_of_fame(img_file_name):
    st.divider()

    values_2026, percent_2026 = predictor_stats()

    root_path = Path(__file__).parent.parent
    img_path = root_path / "img" / img_file_name

    col1, col2 = st.columns([1, 2])
    with col1:
        # Add your photo or a cool avatar
        st.image(img_path, width=200)

    with col2:

        st.markdown(f"### 📅 2026 Season : {percent_2026}")
        st.write(values_2026)

        st.markdown("### 📅 2025 Season : 56.4%")
        st.write("🦜🦜🦜🦜🟢🦜🦜🦜🦜🦜🟢🦜🦜🟢🟢🦜🦜🟢🟢🟢🟢🟢🟢🟢🟢🟢🦜🟢🟢🟢🟢🟢🦜🟢🦜🟢🟢🟢🦜")

        st.markdown("### 📅 2024 Season : 84.6%")
        st.write("🟢🟢🟢🟢🦜🟢🦜🟢🟢🟢🟢🟢🟢")

    st.divider()





