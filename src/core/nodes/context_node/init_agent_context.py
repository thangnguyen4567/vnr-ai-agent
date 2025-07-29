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

        if not state.get("configs", {}).get(agent_id):
            state["configs"] = {}
            state["agent_id"] = agent_id

            return self._init_agent_context(state, agent_id, env)

    def _init_agent_context(self, state: AgentState, agent_id: str, env: str = "production"):

        try:
            agent_config = agent_config_loader.get_config_for_agent_id(agent_id)

            if not agent_config:
                error_message = f"Agent config not found for agent_id: {agent_id}"
                raise ValueError(error_message)
            
            agent_type = agent_config.get("type")
            state["configs"][agent_id] = agent_config

            if agent_type == "fc":
                tools, http_tool_registry = tool_initializer.initialize_tools(agent_config)

                state["configs"][agent_id]["tools"] = tools
                if http_tool_registry:
                    state["configs"][agent_id]["http_tool_registry"] = http_tool_registry

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

                for a in agents:
                    if a["agent_id"] not in state["configs"]:
                        self._init_agent_context(state, a["agent_id"], env)
                
            return state
        
        except Exception as e:
            raise e


