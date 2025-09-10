from src.core.nodes.base_node import BaseNode
from src.core import AgentState
from langchain_core.runnables import RunnableConfig
from typing import Dict, Any
from src.core.nodes.utils.model_utils import get_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from src.core.nodes.utils.message_utils import organize_messages, extract_text_content
from src.prompt import SYSTEM_INFO_PROMPT, HRM_UI_PROMPT
from src.vectordb.vectordb import VectorDBManager
class LLMUIHandler(BaseNode):
    def __init__(self):
        self.vector_db = VectorDBManager()
        self.screen_schema = {}

    def process(
        self, 
        state: AgentState, 
        config: RunnableConfig
    ) -> Dict[str, Any]:
        """
        Bước xử lý tin nhắn người dùng và trả về kết quả của tool call

        Args:
            state: Trạng thái hiện tại của agent
            config: Cấu hình của agent

        Returns:
            Trạng thái mới của agent sau khi xử lý
        """

        # Lấy thông tin người dùng từ cấu hình xml
        sys_config = config.get("configurable",{})
        user_info = sys_config.get("user_info",{})
        agent_id = state.get("agent_id")
        agent_config = state.get("configs",{}).get(agent_id)
        llm_config = agent_config["nodes"]["llm"]
        tools = agent_config.get("tools",[])
        
        sys_config["current_screen"] = user_info.get("current_screen","")

        # Lấy cấu hình LLM từ cấu hình xml
        system_prompt =  HRM_UI_PROMPT + SYSTEM_INFO_PROMPT
        max_turns = llm_config.get("max_turns", 15)
        
        # Sắp xếp tin nhắn theo thứ tự
        new_messages = organize_messages(state["messages"], max_turns)

        if new_messages and isinstance(new_messages[-1], HumanMessage):
            last_message = new_messages[-1]
            message_content = extract_text_content(last_message.content)

            if message_content.strip() == "/restart":
                return {"messages": []}

        prompt = system_prompt.format(**sys_config)
        # Thêm Prompt hệ thống vào đầu tin nhắn
        messages = [SystemMessage(content=prompt)] + new_messages        
        llm_model = get_model(**llm_config)
        response = llm_model.invoke(messages,tools=tools)

        return {"messages": [response]}