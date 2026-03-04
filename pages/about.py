import streamlit as st

st.set_page_config(
    page_title="about",
    page_icon="📝",
    layout="wide" # This makes your graphs look better on desktop
)

st.title("🎰 Behind Scenes")

def about_page():

    st.divider()

    col1, col2 = st.columns([1, 2])
    with col1:
        # Add your photo or a cool avatar
        st.image("https://api.dicebear.com/7.x/bottts/svg?seed=Kalyan", width=200)

    with col2:
        st.markdown("""
        ### Hi, We are group of 6 friends + 1 predictor! 
        

        we built this platform because keeping track of bets in WhatsApp groups is a nightmare and the old google site was static and need manual intervention for updating status.

        ** Mission 2026 :**
        1. Automated tracking so nobody can lie.
        2. Real-time "Ups and Downs" to hurt your ego.
        3. cleaner UI so you can lose your money in style.

        **Tech Stack:** Python, Streamlit, G-sheets, GCP-API
        """)
    st.divider()

    st.info("Found a bug 🐞 ? Too late to inform.")

about_page()