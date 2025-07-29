import streamlit as st
from chatbot import chatbot
from config import config
from flowchart import flowchart
# --- Khởi tạo giá trị page mặc định ---
if "page" not in st.session_state:
    st.session_state.page = "agent"

# --- Sidebar menu ---
with st.sidebar:
    st.markdown("## 📋 Menu")
    if st.button("Agent Chatbot"):
        st.session_state.page = "agent"
    if st.button("Agent Config"):
        st.session_state.page = "agent_config"
    if st.button("Agent Flow"):
        st.session_state.page = "agent_flow"


if st.session_state.page == "agent":
    chatbot()

elif st.session_state.page == "agent_config":
    config()

elif st.session_state.page == "agent_flow":
    flowchart()