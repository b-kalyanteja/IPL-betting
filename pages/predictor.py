import streamlit as st
import time
from utils.players import predictor
from utils.predictor_hall_of_fame import hall_of_fame
from utils.prediction_daily import prediction_next_match



st.set_page_config(
    page_title=" 🧞‍♂️predictor stats",
    page_icon="🧞‍♂️",
    layout="wide" # This makes your graphs look better on desktop
)

st.title("🧞‍♂️ Predictor's Dashboard")


hall_of_fame(img_file_name="predictor.png")

st.markdown("##### *Official match predictor + Committee member. **Trusting this is subjected to financial risks**")


st.divider()
# --- 2. LOGIN LOGIC  PRIVATE SESSION ---

if not st.user.get("is_logged_in"):
    # STATE 1: Not Logged In
    st.info("📍 Log in to predict")
    if st.button("Login with Google"):
        st.login("google")

else:
    current_email = st.user.get("email")

    if current_email not in predictor:
        st.error(f" ⚠️ STAY AWAY ఇది 🧞‍♂️ ( మున్నా ) కి మాత్రమే")
        time.sleep(1)

        st.logout()
        st.rerun()
        st.stop()  #  CRITICAL: This kills the script here so the form never shows

    else:
        # STATE 3: Logged in and Authorized
        st.write(f" 🧞‍♂️ Predictor: **{current_email}**")

        if st.button("Log out"):
            st.session_state.clear()  # added newly
            st.logout()
            st.rerun()

        st.write("humbak")
        #prediction_next_match()

st.divider()
st.divider()

