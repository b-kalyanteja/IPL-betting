players = ["b.kalyanteja@gmail.com", "mvr08626@gmail.com"]

def verify_user(user_email):
    if user_email not in players:
        st.error(f"🚫 Access Denied: {user_email} is not a player")
        st.stop()
     return True