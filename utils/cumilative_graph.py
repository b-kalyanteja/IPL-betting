import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit import cache_data
from streamlit.components.v1 import components
from utils.logos import logos_map
from streamlit_gsheets import GSheetsConnection
from utils.players import player_images

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
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_status = conn.read(worksheet="2026_status", ttl=0)

    # 1. Collect and Sort Data
    players_data = []
    for player in df_status.columns:
        st.write(player)
        try:
            amt = float(df_status[player].iloc[0])
            img = player_images.get(player.lower())
        except:
            amt, img = 0.0, ""
        players_data.append({"amt": amt, "img": img})

    # Sort: Highest profit first
    players_data = sorted(players_data, key=lambda x: x['amt'], reverse=True)

    # 2. Build Flat HTML (Flexbox for horizontal scrolling)
    # This prevents stacking on mobile
    html = '<div style="display: flex; overflow-x: auto; gap: 10px; padding: 10px; white-space: nowrap; scrollbar-width: none;">'

    for i, p in enumerate(players_data):
        color = "#00FFCC" if p['amt'] >= 0 else "#FF4B4B"
        # Assign medals for top 3
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i + 1}"

        # Build individual card
        card = f'<div style="flex: 0 0 auto; text-align: center; background: #1E1E1E; padding: 10px; border-radius: 15px; border: 1px solid #333; min-width: 80px;">'
        card += f'<div style="font-size: 12px; margin-bottom: 5px;">{medal}</div>'
        card += f'<img src="{p["img"]}" style="width: 55px; height: 55px; border-radius: 50%; border: 2px solid {color}; object-fit: cover;">'
        card += f'<div style="font-size: 14px; font-weight: bold; color: {color}; margin-top: 5px;">₹{int(p["amt"])}</div>'
        card += '</div>'
        html += card

    html += '</div>'

    # 3. Render flat string
    st.markdown(html.replace("\n", ""), unsafe_allow_html=True)