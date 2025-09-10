import streamlit as st
from ui.chatbot import chatbot
from ui.config_ui import agent_config, execution_config
from ui.flowchart import flowchart
from ui.logs import show_logs

# --- Page config ---
st.set_page_config(layout="wide")
# --- Khởi tạo giá trị page mặc định ---
if "page" not in st.session_state:
    st.session_state.page = "agent"

# --- Sidebar menu ---
with st.sidebar:
    st.markdown("## 📋 Menu")
    if st.button("Test Agent Chatbot"):
        st.session_state.page = "agent"
    if st.button("Cấu hình Agent"):
        st.session_state.page = "agent_config"
    if st.button("Cấu hình thực thi"):
        st.session_state.page = "execution_config"
    # if st.button("Agent Flow"):
    #     st.session_state.page = "agent_flow"
    if st.button("Log HTTP"):
        st.session_state.page = "logs"

    st.markdown("[Monitor Agent](http://localhost:3000/langfuse)", unsafe_allow_html=True)
    st.markdown("[Config Workflow](http://localhost:8000/dify)", unsafe_allow_html=True)


if st.session_state.page == "agent":
    chatbot()

elif st.session_state.page == "agent_config":
    agent_config()

elif st.session_state.page == "execution_config":
    execution_config()

elif st.session_state.page == "agent_flow":
    flowchart()

elif st.session_state.page == "logs":
    show_logs()