import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit import cache_data
from utils.logos import logos_map
from streamlit_gsheets import GSheetsConnection


def performance_graph():
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Adjust worksheet name to wherever your daily profit/loss is stored
    df_0 = conn.read(worksheet="2026_bets_raw", ttl=0)

    # 2. Clean data: Get the 'Amount' column and remove NaNs
    # Assuming 'Amount' is in column index 8 (adjust as needed)
    df_clean = df.iloc[:, [4, 8]].dropna()  # Column 4=Date, Column 8=Amount
    df_clean.columns = ['Date', 'Amount']

    # 3. Calculate Cumulative Sum (The "Running Total")
    df_clean['Cumulative'] = df_clean['Amount'].cumsum()

    # 4. Create the Plotly Line Graph
    fig = px.line(
        df_clean,
        x='Date',
        y='Cumulative',
        markers=True,  # Adds dots on each data point
        template="plotly_dark"  # Matches your dark theme
    )

    # 5. Styling for "Beauty" and "Mobile Static"
    fig.update_traces(
        line_color='#00FFCC',  # Neon cyan/green
        line_width=3,
        marker=dict(size=8, color='white', line=dict(width=2, color='#00FFCC'))
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,  # Good height for mobile
        # THE MAGIC: Disable all touch/mouse interaction
        dragmode=False,
        hovermode=False,
        xaxis=dict(showgrid=False, title="Timeline"),
        yaxis=dict(showgrid=True, gridcolor='#333', title="Amount (₹)"),
    )

    # 6. Display in Streamlit
    # use_container_width makes it responsive for mobile/laptop
    st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})


# Call the function in your app
cumulative_balance_graph()