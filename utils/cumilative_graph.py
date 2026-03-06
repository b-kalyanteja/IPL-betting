import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit import cache_data
from streamlit.components.v1 import components
from utils.logos import logos_map
from streamlit_gsheets import GSheetsConnection

@st.cache_data(ttl=300)
def performance_graph():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_03 = conn.read(worksheet="2026_cumilative", ttl=0)

    import plotly.graph_objects as go
    fig = go.Figure()

    for player in df_03.columns:

        y_data = df_03[player].dropna().tolist()
        x_data = list(range(len(y_data)))
        if y_data:
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines+markers',
                name=player.title(),  # Capitalizes names (e.g., 'kalyan' -> 'Kalyan')
                line=dict(width=3),
                marker=dict(size=6)
            ))

    # 4. Professional Styling
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=10),
        height=350,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1),

        xaxis=dict(showgrid=False, dtick=1,tickformat="d",title="Matches",fixedrange=True),
        yaxis=dict(showgrid=True, gridcolor='#333', title="Earnings (zl)",fixedrange=True),
        hovermode="x unified",
        dragmode=False,
    )

    st.plotly_chart(fig,
                    use_container_width=True,
                    config = {
                        'staticPlot': False,
                        'displayModeBar': False,
                        'scrollZoom': False
                    })



@st.cache_data(ttl=300)
def current_status():
    # 1. Read the latest cumulative data
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_status = conn.read(worksheet="2026_status", ttl=0)

    st.markdown("##### 🏆 LiveLeaderboard")

    cols = st.columns(3)
    players = df_status.columns.tolist()

    for i, player in enumerate(players):
        col_index = i % 3
        with cols[col_index]:
            player_photo = df_status.iloc[0, i]
            try:
                player_amount = df_status.iloc[1, i]
            except IndexError:
                player_amount = 0

            color = "#00FFCC" if float(player_amount) >= 0 else "#FF4B4B"


            st.image(player_photo, use_container_width=True)

            st.markdown(f"""
                    <div style="text-align: center; background-color: #1E1E1E; padding: 10px; border-radius: 0 0 10px 10px; border-top: 2px solid {color};">
                        <div style="font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px;">{player}</div>
                        <div style="font-size: 20px; font-weight: bold; color: {color};">₹{int(player_amount)}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.write("")
