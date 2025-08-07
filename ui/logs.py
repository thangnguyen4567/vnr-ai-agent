import streamlit as st

def show_logs():
    st.set_page_config(layout="wide")
    with open('logs/dev.log', 'r') as file:
        logs = file.read()
    st.text_area('Logs', logs, height=700)
    
