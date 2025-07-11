import streamlit as st
from src.core.multi_agent import multi_agent_graph as graph
import asyncio
from typing import AsyncGenerator
from src.core.config_loader import agent_config_loader
from langfuse.langchain import CallbackHandler
from src.config import settings
from langfuse import Langfuse
import streamlit.components.v1 as components

# Thiết lập tiêu đề ứng dụng
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# Thiết lập loại agent là multi_agent
agent_config_loader.set_agent_type("multi")

# Khởi tạo chat history trong session state nếu chưa có
if "messages" not in st.session_state:
    st.session_state.messages = []

# Khởi tạo config trong session state nếu chưa có
if "config" not in st.session_state:
    Langfuse(
        public_key=settings.LANGFUSE_CONFIG["public_key"],
        secret_key=settings.LANGFUSE_CONFIG["secret_key"],
        host=settings.LANGFUSE_CONFIG["host"],
    )
    langfuse_handler = CallbackHandler()
    st.session_state.config = {
        "configurable": {
            "current_date": "06/06/2025",
            "language": "vi-VN",
            "agent_id": "",
            "thread_id": "113",
            "user_info": {
                "name": "Nguyễn Văn A",
                "employee_id": "EMP001"
            }
        },
        "callbacks": [langfuse_handler],
        "recursion_limit": 10,
    }


async def process_message():
    full_response = ""
    async for event in graph.astream_events(inputs, config=st.session_state.config):
        kind = event["event"]

        if kind == "on_custom_event":
            thinking_content = event["data"]["data"]["text"]
            yield thinking_content

        elif kind == "on_chat_model_stream" and event["metadata"].get(
            "langgraph_node"
        ) not in ["research", "reflection", "router_agent"]:
            answer_content = event["data"]["chunk"].content
            if answer_content:
                full_response += answer_content
                yield answer_content
    
    # Lưu tin nhắn của bot vào lịch sử sau khi xử lý xong
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})


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

# Hàm để tự động cuộn xuống cuối trang
def auto_scroll_to_bottom():
    js = '''
    <script>
        function scroll_to_bottom() {
            window.scrollTo(0, document.body.scrollHeight);
        }
        scroll_to_bottom();
    </script>
    '''
    components.html(js, height=0)

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
        response = st.write_stream(to_sync_generator(process_message()))
        
    # Tự động cuộn xuống cuối trang sau khi có phản hồi
    auto_scroll_to_bottom()
