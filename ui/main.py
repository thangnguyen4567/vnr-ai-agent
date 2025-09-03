import streamlit as st
from chatbot import chatbot
from config import config
from flowchart import flowchart
from logs import show_logs
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
    # if st.button("Agent Flow"):
    #     st.session_state.page = "agent_flow"
    if st.button("Http logs"):
        st.session_state.page = "logs"

    st.markdown("[Monitor Agent](http://localhost:3000/langfuse)", unsafe_allow_html=True)
    st.markdown("[Config Workflow](http://localhost:8000/dify)", unsafe_allow_html=True)


if st.session_state.page == "agent":
    chatbot()

elif st.session_state.page == "agent_config":
    config()

elif st.session_state.page == "agent_flow":
    flowchart()

elif st.session_state.page == "logs":
    show_logs()