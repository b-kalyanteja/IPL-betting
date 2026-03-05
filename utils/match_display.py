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

    with st.container(border=True):
        col1, col_vs, col2 = st.columns([2, 1, 2])
        with col1:
            st.markdown(f"""
                <div style="text-align: center;">
                    <img src="{logo_1}" width="80" style="border-radius: 50%; background: white; padding: 5px;">
                    <h3 style="margin-bottom: 0;">{team_1_name}</h3>
                    <div style="font-size: 20px;">{t1_icons}</div>
                </div>
            """, unsafe_allow_html=True)

        with col_vs:
            st.markdown("""
                <div style="text-align: center; margin-top: 40px;">
                    <h2 style="color: #888;">VS</h2>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style="text-align: center;">
                    <img src="{logo_2}" width="80" style="border-radius: 50%; background: white; padding: 5px;">
                    <h3 style="margin-bottom: 0;">{team_2_name}</h3>
                    <div style="font-size: 20px;">{t2_icons}</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()



