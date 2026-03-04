import streamlit as st
from utils.predictor_hall_of_fame import hall_of_fame, predictor_stats
from utils.prediction import values_2026, percent_2026

from utils.sheets_data import df_07


st.set_page_config(
    page_title="predictor",
    page_icon="🧞‍♂️",
    layout="wide" # This makes your graphs look better on desktop
)

st.title("🧞‍♂️ Predictor's Dashboard")


hall_of_fame(img_file_name="predictor.png", percent_2026=percent_2026, values_2026=values_2026)

st.divider()

#predictor_stats()
def predictor_statsss():

    prediction_results= df_07.iloc[0:77, 7]
    r_list: list = prediction_results.tolist()
    st.write(r_list)

predictor_statsss()

st.divider()

if not st.user.get("is_logged_in"):
    # STATE 1: Not Logged In
    st.info("Login to place bets")
    if st.button("Log in with Google 🌐"):
        st.login("google")
else:
    current_email = st.user.get("email")


