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
            x=1
        ),
        xaxis=dict(showgrid=False, dtick=1,tickformat="d",title="Matches"),
        yaxis=dict(showgrid=True, gridcolor='#333', title="Earnings (zl)"),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)



def current_status():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-m3xGBp4kDPQgG4-ZzockJy3E--gqPEFJGTtonfdfDX9Juuga0O0UPxTCUUPLmiNX_Op8kkEH0G_j/pubhtml?gid=642106326&single=true&widget=true&headers=false"

    # Using Streamlit columns to center the content
    col1, col2, col3 = st.columns([1, 8, 1])

    with col2:
        st.markdown("##### 📅 Schedule & Points Table")
        components.html(f"""
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                width: 100%;
                border: 1px solid #333; 
                border-radius: 15px; 
                overflow: hidden;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            ">
                <iframe src="{sheet_url}" 
                        width="100%" 
                        height="400" 
                        style="border: none;" 
                        scrolling="yes">
                </iframe>
            </div>
        """, height=400)
