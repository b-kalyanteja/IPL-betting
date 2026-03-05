import streamlit as st
from utils.logos import logos_map

def match_widget(team_1, team_2, t1_bets,t2_bets):

    logo_1 = logos_map.get(team_1)
    logo_2 = logos_map.get(team_2)

    team_1_name = team_1.upper()
    team_2_name = team_2.upper()

    t1_icons = ("👤" * t1_bets)
    t2_icons = ("👤" * t2_bets)

    with st.container(border=True):

        col1, col_vs, col2 = st.columns([2, 1, 2])

        with col1:
            st.image(logo_1, width=80)
            st.write(f"### {team_1_name}")
            st.write(t1_icons)

        with col_vs:
            st.write("")
            st.write("")
            st.header("VS")

        with col2:
            st.image(logo_2, width=80)
            st.write(f"### {team_2_name}")
            st.write(t2_icons)

    st.divider()



