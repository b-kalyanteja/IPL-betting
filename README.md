
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine ( local)

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```


# 🏏 IPL 2026 Betting Dashboard

A real-time Streamlit application integrated with Google Sheets to manage authorized betting for IPL 2026.

## ⚙️ Logic Workflow

1.  **Authentication**: Users log in via Google OAuth.
2.  **Authorization**: The app checks the user's email against a hardcoded `AUTHORIZED_PLAYERS` set.
    * *If unauthorized*: The app triggers a "Sannasi" logout flow with a 1-second delay to clear browser cookies.
3.  **Data Fetching**: 
    * Fetches the `2026_summary` sheet for cumulative performance.
    * Fetches the `2026_bets` sheet to track historical wagers.
    * Fetches the `2026_schedule` to identify today's active matches.
4.  **Match Manager**: 
    * Automatically filters for matches happening **today** where the `Result` column is empty.
    * Dynamically generates betting forms for Match 1 and Match 2.
5.  **Submission**: 
    * New bets are appended to the local DataFrame using `pd.concat`.
    * The updated table is pushed to Google Sheets via `connection.update()`.
6.  **Visualization**: 
    * Displays a multi-line "Ups and Downs" cumulative graph.
    * Shows a mobile-optimized "Total Pot" metric and status image.

## 🛠 Tech Stack
* **Frontend**: Streamlit
* **Database**: Google Sheets (via `st.connection`)
* **Data Handling**: Pandas