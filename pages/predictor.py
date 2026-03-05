import streamlit as st
from utils.predictor_hall_of_fame import hall_of_fame , predictor_stats

from utils.sheets_data import df_04


st.set_page_config(
    page_title="🧞‍predictor stats",
    page_icon="🧞‍♂️",
    layout="wide" # This makes your graphs look better on desktop
)

st.title("🧞‍♂️ Predictor's Dashboard")


hall_of_fame(img_file_name="predictor.png")

st.markdown("##### *Official match predictor + Committee member. **Trusting this is subjected to financial risks**")

if not st.user.get("is_logged_in"):

    st.info("Login to Predict")
    if st.button("Google 🌐"):
        st.login("google")
else:
    current_email = st.user.get("email")


