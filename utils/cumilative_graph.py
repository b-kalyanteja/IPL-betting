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

    table_html = """
        <table style="width: 100%; border-collapse: separate; border-spacing: 8px; table-layout: fixed;">
        """

    # 3. Create the grid (3 players per row)
    for i in range(0, len(players), 3):
        table_html += "<tr>"

        # Get the next 3 players
        row_slice = players[i: i + 3]

        for player in row_slice:
            # Pull dynamic values
            # Row 2 (Index 0) = Amount | Row 3 (Index 1) = URL
            raw_amount = df_status[player].iloc[0]
            img_url = df_status[player].iloc[1]

            try:
                amt_val = float(raw_amount)
            except:
                amt_val = 0.0

            color = "#00FFCC" if amt_val >= 0 else "#FF4B4B"

            # Add player cell
            table_html += f"""
                <td style="background-color: #1E1E1E; border-radius: 12px; padding: 12px 5px; text-align: center; border: 1px solid #333;">
                    <img src="{img_url}" style="width: 65px; height: 65px; border-radius: 50%; border: 2px solid {color}; object-fit: cover;">
                    <div style="font-size: 10px; color: #888; margin-top: 8px; font-weight: bold;">{player.upper()}</div>
                    <div style="font-size: 16px; font-weight: bold; color: {color};">₹{int(amt_val)}</div>
                </td>
                """

        # If a row has fewer than 3 players (e.g., you have 5 total),
        # we add empty cells to keep the layout aligned
        while len(row_slice) < 3:
            table_html += "<td></td>"
            row_slice.append(None)

        table_html += "</tr>"

    table_html += "</table>"

    # 4. Render the final table
    st.markdown(table_html, unsafe_allow_html=True)