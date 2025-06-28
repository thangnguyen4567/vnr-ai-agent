import streamlit as st
from dotenv import load_dotenv
from src.core.multi_agent import multi_agent_graph as graph
import asyncio
from typing import AsyncGenerator
from src.core.config_loader import agent_config_loader
# Load biến môi trường
load_dotenv()

# Thiết lập tiêu đề ứng dụng
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")
agent_config_loader.set_agent_type("multi")
# Khởi tạo chat history trong session state nếu chưa có
if "messages" not in st.session_state:
    st.session_state.messages = []

# Khởi tạo config trong session state nếu chưa có
if "config" not in st.session_state:
    st.session_state.config = {
        'user_id': '1234567890',
        'user_name': 'Thang',
        'current_date': '06/06/2025',
        'language': 'vi-VN',
        'agent_id': 'd4e12d5bb4014794fa3f956e2b0e01cf'
    }

async def process_message():
    async for event in graph.astream_events(inputs, config=st.session_state.config):
        kind = event['event']

        if kind == "on_custom_event":
            thinking_content = event['data']['data']['text']
            yield thinking_content

        elif kind == "on_chat_model_stream" and event["metadata"].get("langgraph_node") not in ["research","reflection"]:
            answer_content = event['data']['chunk'].content
            if answer_content:
                yield answer_content

def to_sync_generator(async_gen: AsyncGenerator):
    # 1. Tạo mới một loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        while True:
            try:
                # Chạy 1 bước của async gen
                yield loop.run_until_complete(async_gen.__anext__())
            except StopAsyncIteration:
                break
    finally:
        # Hủy loop khi xong
        loop.close()
        # Trả lại setting ban đầu (nếu cần)
        asyncio.set_event_loop(None)


# Hiển thị tin nhắn trước đó
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Giao diện chat
if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
    # Thêm tin nhắn người dùng vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Hiển thị đang xử lý
    with st.chat_message("assistant"):
        inputs = {"messages": [("user", prompt)]}
        message_placeholder = st.empty()
        response = st.write_stream(to_sync_generator(process_message()))





