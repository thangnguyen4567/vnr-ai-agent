from src.core.nodes.base_node import BaseNode
from src.core import AgentState
from langchain_core.runnables import RunnableConfig
from typing import Dict, Any
from src.core.nodes.utils.model_utils import get_model
from langchain_core.messages import HumanMessage, SystemMessage
from src.core.nodes.utils.message_utils import organize_messages, extract_text_content
from src.prompt import HRM_CHATBOT_PROMPT, SYSTEM_INFO_PROMPT, USER_INFO_PROMPT, HRM_TOOL_CALL_PROMPT

class LLMHandler(BaseNode):

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

        if not agent_config:
            raise ValueError(f"Agent config not found for agent_id: {agent_id}")
        
        user_info_str = self.__format_user_info(user_info)

        # Lấy cấu hình LLM từ cấu hình xml
        llm_config = agent_config["nodes"]["llm"]
        agent_prompt = llm_config.get("agent_prompt","")
        system_prompt =  HRM_TOOL_CALL_PROMPT + SYSTEM_INFO_PROMPT + user_info_str + agent_prompt
        max_turns = llm_config.get("max_turns", 15)
        tools = agent_config.get("tools",[])
        
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
        response = llm_model.invoke(messages, tools=tools)

        return {"messages": [response]}
    

    async def aggregate_result(
        self, 
        state: AgentState, 
        config: RunnableConfig
    ) -> Dict[str, Any]:
        """
        Xử lý tin nhắn người dùng và trả về kết quả cuối cùng
        Args:
            state: Trạng thái hiện tại của agent
            config: Cấu hình của agent

        Returns:
            Trạng thái mới của agent sau khi xử lý
        """
        # Xử lý thông tin config
        sys_config = config.get("configurable",{})
        user_info = sys_config.get("user_info",{})
        llm_config = {"provider": "openai"}
        user_info_str = self.__format_user_info(user_info)
        max_turns = 15

        # Tạo prompt hệ thống
        system_prompt = HRM_CHATBOT_PROMPT + SYSTEM_INFO_PROMPT + user_info_str

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

        llm_model = get_model(config=llm_config)
        response = llm_model.invoke(messages)

        return {"messages": [response]}

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