import logging
from sys import version
from typing import Dict, Any
from src.core.multi_agent import multi_agent_graph
from src.core.fc_agent import fc_agent_graph
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv
from src.utils.common import AgentType

load_dotenv()

# Logger
logger = logging.getLogger(__name__)


class ChatService:
    """Service xử lý các yêu cầu AI"""

    def __init__(self):
        """Khởi tạo service"""
        logger.info("Khởi tạo AI Service")

    @staticmethod
    def parse_start_event(event):
        """
        Parse event từ LangGraph để chuyển đổi thành JSON serializable

        Args:
            event: Sự kiện bắt đầu từ LangGraph

        Returns:
            Dict/list/str: chứa thông tin về sự kiện đã được chuyển đổi
        """
        if isinstance(event, dict):
            return {k: ChatService.parse_start_event(v) for k, v in event.items()}
        elif isinstance(event, list):
            return [ChatService.parse_start_event(item) for item in event]
        elif isinstance(event, tuple):
            return tuple(ChatService.parse_start_event(item) for item in event)
        elif isinstance(event, str):
            return event
        else:
            try:
                return event.__dict__
            except:
                return event

    @staticmethod
    async def agent_stream_response(input: Dict[str, Any], config: Dict[str, Any]):
        """
        Xử lý yêu cầu AI với stream response

        Args:
            input: Câu hỏi hoặc nhiệm vụ cho AI
            config: Cấu hình cho AI

        Returns:
            json: phản hồi từ AI
        """
        if config["agent_type"] == AgentType.SINGLE_AGENT.value:
            graph = fc_agent_graph
        elif config["agent_type"] == AgentType.MULTI_AGENT.value:
            graph = multi_agent_graph

        async for event in graph.astream_events(input, config=config, version="v2"):
            kind = event["event"]

            if kind == "on_custom_event":
                thinking_content = event["data"]["data"]["text"]
                yield thinking_content

            elif kind == "on_chat_model_stream" and event["metadata"].get(
                "langgraph_node"
            ) not in ["research", "reflection", "router_agent"]:
                answer_content = event["data"]["chunk"].content
                if answer_content:
                    yield answer_content

    @staticmethod
    def agent_response():
        pass

    @staticmethod
    def get_langfuse_handler() -> CallbackHandler:
        """
        Tạo Langfuse handler cho tracking

        Args:
            session_id: ID của phiên làm việc
            config: Cấu hình cho AI
            langfuse_config: Cấu hình Langfuse (nếu có)

        Returns:
            CallbackHandler hoặc None nếu không có đủ thông tin cấu hình
        """

        langfuse_handler = CallbackHandler()
        return langfuse_handler
