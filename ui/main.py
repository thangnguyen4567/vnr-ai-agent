import streamlit as st
from ui.views.chatbot import chatbot
from ui.views.agents_overview import render_agents_overview
from ui.views.agent_detail import render_agent_detail
from ui.views.execution_config import execution_config
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
    if st.button("Log HTTP"):
        st.session_state.page = "logs"

    st.markdown("[Monitor Agent](http://localhost:3000/langfuse)", unsafe_allow_html=True)
    st.markdown("[Config Workflow](http://localhost:8000/dify)", unsafe_allow_html=True)


if st.session_state.page == "agent":
    chatbot()

elif st.session_state.page == "agent_config":

    if "agent_config_view" not in st.session_state:
        st.session_state.agent_config_view = "overview"
        
    if st.session_state.agent_config_view == "overview":
        render_agents_overview()
    else:
        render_agent_detail()

elif st.session_state.page == "execution_config":
    execution_config()

elif st.session_state.page == "agent_flow":
    flowchart()

elif st.session_state.page == "logs":
    show_logs()