import streamlit as st
from utils.prediction import values_2026, percent_2026
import os


st.set_page_config(
    page_title="about",
    page_icon="🧞‍♂️",
    layout="wide" # This makes your graphs look better on desktop
)

st.title("🧞‍♂️ Predictor's Dashboard")



def hall_of_fame():
    st.divider()

    current_dir = os.path.dirname(__file__)
    img_path = os.path.join(current_dir,".." "img", "predictor.png")

    col1, col2 = st.columns([1, 2])
    with col1:
        # Add your photo or a cool avatar
        st.image("img_path", width=200)

    with col2:
        st.markdown("### 📅 2024 Season")
        st.write("🟢🟢🟢🟢🦜🟢🦜🟢🟢🟢🟢🟢🟢")
        st.metric(label="Win Percentage", value="84.6%")

        st.markdown("### 📅 2025 Season")
        st.write("🦜🦜🦜🦜🟢🦜🦜🦜🦜🦜🟢🦜🦜🟢🟢🦜🦜🟢🟢🟢🟢")
        st.metric(label="Win Percentage", value="38.1%")

        st.markdown("### 📅 2026 Season")
        st.write(values_2026)
        st.metric(label="Win Percentage", value= percent_2026)

    st.divider()

hall_of_fame()


if not st.user.get("is_logged_in"):
    # STATE 1: Not Logged In
    st.info("Login to place bets")
    if st.button("Log in with Google 🌐"):
        st.login("google")
else:
    current_email = st.user.get("email")


