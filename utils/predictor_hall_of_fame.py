import streamlit as st
from pathlib import Path
from utils.sheets_data import df_04


def hall_of_fame(img_file_name, percent_2026, values_2026):
    st.divider()

    root_path = Path(__file__).parent.parent
    img_path = root_path / "img" / img_file_name

    col1, col2 = st.columns([1, 2])
    with col1:
        # Add your photo or a cool avatar
        st.image(img_path, width=200)

    with col2:
        st.markdown("### 📅 2024 Season : 84.6%")
        st.write("🟢🟢🟢🟢🦜🟢🦜🟢🟢🟢🟢🟢🟢")

        st.markdown("### 📅 2025 Season : 38.1%")
        st.write("🦜🦜🦜🦜🟢🦜🦜🦜🦜🦜🟢🦜🦜🟢🟢🦜🦜🟢🟢🟢🟢")

        st.markdown(f"### 📅 2026 Season : {percent_2026}")
        st.write(values_2026)

    st.divider()



def predictor_stats():

    prediction_list = df_04.iloc[0:77, 7].astype(str).tolist()
    st.write(prediction_list)