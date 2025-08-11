import streamlit as st

def show_logs():
    st.set_page_config(layout="wide")
    try:
        with open('logs/dev.log', 'r') as file:
            lines = file.readlines()
            logs = ''.join(lines[-10:]) if lines else ""
    except Exception as e:
        logs = f"Lỗi khi đọc file log: {str(e)}"
    st.text_area('Logs', logs, height=800)
    
