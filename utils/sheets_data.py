import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Establish connection
conn = st.connection("gsheets", type=GSheetsConnection)


df_01 = conn.read(worksheet="2026_summary", ttl=1)
df_02 = conn.read(worksheet="2026_bets",  ttl=1)
df_03 = conn.read(worksheet="2026_cumilative", ttl=1)
df_04 = conn.read(worksheet="2026_bets_raw", ttl=1)
df_05 = conn.read(worksheet="2026_bets_log", ttl=1)
df_06 = conn.read(worksheet="2026_prediction", ttl=1)
df_07 = conn.read(worksheet="2026_schedule", ttl=1)
df_08 = conn.read(worksheet="2026_status", ttl=1)
df_09 = conn.read(worksheet="2026_today", ttl=1)


#TODO
#shorten the list by using dictionary

#sheets = [ "2026_summary", "2026_bets", "2026_cumilative",]
#df={}
# df[x] = conn.read(worksheet = sheets[x], ttl =1)