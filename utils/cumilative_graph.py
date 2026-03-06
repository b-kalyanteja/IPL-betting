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

    players_data = []
    for player in df_status.columns:
        try:
            amt = float(df_status[player].iloc[0])
            img = df_status[player].iloc[1]
        except:
            amt, img = 0.0, ""
        players_data.append({"name": player, "amt": amt, "img": img})

    players_data = sorted(players_data, key=lambda x: x['amt'], reverse=True)

    # 2. Build the HTML without any internal indentation
    html = '<div style="background-color: #111; padding: 10px; border-radius: 15px;"><table style="width: 100%; border-collapse: collapse;">'

    for i, p in enumerate(players_data):
        color = "#00FFCC" if p['amt'] >= 0 else "#FF4B4B"
        rank = f"#{i + 1}"

        # We add each row as a single flat string
        row = f'<tr style="border-bottom: 1px solid #222;">'
        row += f'<td style="padding: 10px; width: 30px; font-weight: bold; color: #888; font-size: 12px;">{rank}</td>'
        row += f'<td style="padding: 5px; width: 55px;"><img src="{p["img"]}" style="width: 45px; height: 45px; border-radius: 50%; border: 2px solid {color}; object-fit: cover;"></td>'
        row += f'<td style="padding: 10px; text-align: left;"><div style="font-size: 14px; font-weight: bold; color: white;">{p["name"]}</div></td>'
        row += f'<td style="padding: 10px; text-align: right;"><div style="font-size: 16px; font-weight: bold; color: {color};">₹{int(p["amt"])}</div></td>'
        row += '</tr>'
        html += row

    html += '</table></div>'

    # 3. Render with all newlines removed to prevent markdown errors
    st.markdown(html.replace("\n", ""), unsafe_allow_html=True)