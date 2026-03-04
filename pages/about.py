print ("hello")


def show_about_page():
    st.title("👨‍💻 The Brain Behind the Bets")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Add your photo or a cool avatar
        st.image("https://api.dicebear.com/7.x/bottts/svg?seed=Kalyan", width=150)

    with col2:
        st.markdown("""
        ### Hi, I'm [Your Name]! 
        *Chief Sannasi Officer (CSO)*

        I built this platform because keeping track of bets in WhatsApp groups is a nightmare and someone always "forgets" how much they owe.

        **My Mission:**
        1. Automated tracking so nobody can lie.
        2. Real-time "Ups and Downs" to hurt your ego.
        3. A clean UI so you can lose your money in style.

        **Tech Stack:** Python, Streamlit, and a very stressed-out Google Sheet.
        """)

    st.info("💡 Found a bug? Don't texll me. Just bet better.")