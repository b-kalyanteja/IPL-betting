import streamlit as st
from utils.prediction import values_2026, percent_2026
from pathlib import Path


st.set_page_config(
    page_title="about",
    page_icon="🧞‍♂️",
    layout="wide" # This makes your graphs look better on desktop
)

st.title("🧞‍♂️ Predictor's Dashboard")



def hall_of_fame():
    st.divider()

    root_path = Path(__file__).parent.parent
    img_path = root_path / "img" / "predictor.png"

    col1, col2 = st.columns([1, 2])
    with col1:
        # Add your photo or a cool avatar
        st.image(img_path, width=200)

    with col2:
        st.markdown("### 📅 2024 Season : 84.6%")
        st.write("🟢🟢🟢🟢🦜🟢🦜🟢🟢🟢🟢🟢🟢")

        st.markdown("### 📅 2025 Season 38.1%")
        st.write("🦜🦜🦜🦜🟢🦜🦜🦜🦜🦜🟢🦜🦜🟢🟢🦜🦜🟢🟢🟢🟢")

        st.markdown(f"### 📅 2026 Season : {percent_2026}")
        st.write(values_2026)

    st.divider()

hall_of_fame()


if not st.user.get("is_logged_in"):
    # STATE 1: Not Logged In
    st.info("Login to place bets")
    if st.button("Log in with Google 🌐"):
        st.login("google")
else:
    current_email = st.user.get("email")


