from src.core.nodes.base_node import BaseNode
from src.core import AgentState
from langchain_core.runnables import RunnableConfig
from typing import Dict, Any
from src.core.nodes.utils.model_utils import get_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from src.core.nodes.utils.message_utils import organize_messages, extract_text_content
from src.prompt import SYSTEM_INFO_PROMPT, USER_INFO_PROMPT, HRM_UI_PROMPT, SCREEN_DESC_TEMPLATE , HRM_UI_SELECT_SCREEN_PROMPT
from src.vectordb.vectordb import VectorDBManager

class LLMUIHandler(BaseNode):
    def __init__(self):
        self.vector_db = VectorDBManager()
        self.screen_schema = {}

    async def process(
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
        # Chọn màn hình phù hợp nhất để xử lý yêu cầu người dùng
        # screen_name = self.__screen_selector(state, llm_config)

        screen_desc = []
        self.screen_schema = self.vector_db.get_documents(state["messages"][-1].content, k=10, index_name="ui_schema")
        for a in self.screen_schema:
            screen_desc.append(SCREEN_DESC_TEMPLATE.format(name=a.metadata["pageId"], description=a.page_content, schema=a))

        sys_config["screen_schema"] = "\n".join(screen_desc)
        sys_config["current_screen"] = user_info.get("current_screen","")

        if not agent_config:
            raise ValueError(f"Agent config not found for agent_id: {agent_id}")
        
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
        response = llm_model.invoke(messages)

        return {"messages": [response]}
    

    def __screen_selector(
        self,
        state: AgentState,
        config: RunnableConfig
    ) -> Dict[str, Any]:
        """
        Chọn màn hình phù hợp nhất để xử lý yêu cầu người dùng

        Args:
            state: Trạng thái hiện tại của agent
            config: Cấu hình của agent

        Returns:
            Màn hình phù hợp nhất để xử lý yêu cầu người dùng
        """
        self.screen_schema = self.vector_db.get_documents(state["messages"][-1].content, k=10, index_name="ui_schema")

        screen_desc = []
        for a in self.screen_schema:
            screen_desc.append(SCREEN_DESC_TEMPLATE.format(name=a.metadata["pageId"], description=a.page_content))

        messages = []
        for msg in state["messages"]:
            if isinstance(msg, AIMessage) and msg.content:
                messages.append(f"assistant: {msg.content}")
            elif isinstance(msg, HumanMessage) and msg.content:
                messages.append(f"user: {msg.content}")

        screen_desc = "\n".join(screen_desc)
        prompt = HRM_UI_SELECT_SCREEN_PROMPT.format(
            screen_desc=screen_desc, 
            chat_history="\n".join(messages[-4:])
        )
        llm_model = get_model(**config)
        response = llm_model.invoke(prompt)

        return response.content

    def __format_user_info(
        self, 
        user_info: Dict[str, Any]
    ) -> str:
        """
        Định dạng thông tin người dùng thành chuỗi

        Args:
            user_info: Thông tin người dùng

        Returns:
            Chuỗi thông tin người dùng đã được định dạng
        """
        if not user_info:
            return ""
        
        user_info_str = USER_INFO_PROMPT + "\n"
        for key, value in user_info.items():
            user_info_str += f"\n **{key}**: {value}\n"

        return user_info_str