from src.core.nodes.base_node import BaseNode
from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from src.core import AgentState
from src.core.config_loader import agent_config_loader
from src.core.tools.register import ToolInitializer

tool_initializer = ToolInitializer()

class ContextInitializer(BaseNode):
    """
        Node khởi tạo ngữ cảnh cho agent
        Lấy cấu hình agent từ AgentConfigLoader
    """
    def __init__(self):
        super().__init__()

    async def process(self, state: AgentState, config: RunnableConfig) -> Dict[str, Any]:

        agent_id = config.get("configurable", {}).get("agent_id")
        env = config.get("configurable", {}).get("env", "production")

        # Kiểm tra xem đã khởi tạo cấu hình agent chưa, nếu chưa thì khởi tạo cấu hình agent
        if not state.get("configs", {}).get(agent_id):
            state["configs"] = {}
            state["agent_id"] = agent_id

            # Khởi tạo cấu hình agent
            return self._init_agent_context(state, agent_id, env)

        # Nếu đã khởi tạo cấu hình agent thì trả về state hiện tại
        return state

    def _init_agent_context(self, state: AgentState, agent_id: str, env: str = "production"):

        try:
            # Lấy cấu hình agent từ AgentConfigLoader
            agent_config = agent_config_loader.get_config_for_agent_id(agent_id)

            if not agent_config:
                error_message = f"Agent config not found for agent_id: {agent_id}"
                raise ValueError(error_message)
            
            # Lấy loại agent
            agent_type = agent_config.get("type")

            # Lưu cấu hình agent vào state
            state["configs"][agent_id] = agent_config

            # Nếu agent là agent FC thì khởi tạo các tool
            if agent_type == "fc" or agent_type == "ui":
                tools, http_tool_registry, store_tool_registry, workflow_tool_registry = tool_initializer.initialize_tools(agent_config)

                state["configs"][agent_id]["tools"] = tools
                # Lưu các tool vào state của agent
                if http_tool_registry:
                    state["configs"][agent_id]["http_tool_registry"] = http_tool_registry
                if store_tool_registry:
                    state["configs"][agent_id]["store_tool_registry"] = store_tool_registry
                if workflow_tool_registry:
                    state["configs"][agent_id]["workflow_tool_registry"] = workflow_tool_registry
                    
            # Nếu agent là agent Multi thì khởi tạo các agent con
            elif agent_type == "multi":
                agents = agent_config.get("sub_agents", [])
                if not agents:
                    error_message = f"Agent config not found for agent_id: {agent_id}"
                    raise ValueError(error_message)
                
                for a in agents:
                    if not a.get("code"):
                        # tạo code từ name của agent theo quy tắc 2 chữ cái đầu tiên của từng từ 
                        a["code"] = "".join([c[0].upper() for c in a.get("name", "").strip().split(" ") if c])

                state["configs"][agent_id]["agents"] = agents

                # Khởi tạo cấu hình agent con
                for a in agents:
                    if a["agent_id"] not in state["configs"]:
                        self._init_agent_context(state, a["agent_id"], env)
                
            return state
        
        except Exception as e:
            raise e


