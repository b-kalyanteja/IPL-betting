
def verify_user(email):
    players = ["b.kalyanteja@gmail.com", "mvr08626@gmail.com"]
    if email not in players:
        st.error(f"🚫 Access Denied: {email} is not a player")
        st.stop()
     return True