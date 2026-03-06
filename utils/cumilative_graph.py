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



#@st.cache_data(ttl=300)
def current_status():
    # 1. Read the latest cumulative data
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_status = conn.read(worksheet="2026_status", ttl=0)

    st.markdown("##### 🏆 Live Leaderboard")

    cols = st.columns(3)
    players = df_status.columns.tolist()

    cols = st.columns(3)

    for i, player in enumerate(players):
        # This keeps the players in a 3-column grid that won't break
        with cols[i % 3]:
            # Adjust indices based on your sheet: Row 2=Amt (0), Row 3=Link (1)
            raw_amt = df_status[player].iloc[0]
            img_url = df_status[player].iloc[1]

            try:
                amt_val = float(raw_amt)
            except:
                amt_val = 0.0

            color = "#00FFCC" if amt_val >= 0 else "#FF4B4B"

            # Use a container-style display for each player
            st.image(img_url, use_container_width=True)
            st.markdown(f"""
                    <div style="text-align: center; background-color: #1E1E1E; padding: 5px; border-radius: 5px; border-bottom: 3px solid {color}; margin-bottom: 15px;">
                        <div style="font-size: 9px; color: #888;">{player.upper()}</div>
                        <div style="font-size: 14px; font-weight: bold; color: {color};">₹{int(amt_val)}</div>
                    </div>
                """, unsafe_allow_html=True)