from .supervisor import RouterNode
from src.core import AgentState
from langchain_core.runnables import RunnableConfig

router_node = RouterNode()
async def router_agent(state: AgentState, config: RunnableConfig):
    """
    Hàm wrapper cho node router_agent để đảm bảo tương thích ngược.

    Args:
        state: Trạng thái hiện tại của agent
        config: Cấu hình của agent

    Returns:
        Kết quả routing
    """
    return router_node._router_agent(state, config)


async def switch_agent(state: AgentState):
    """
    Hàm wrapper cho node switch_agent để đảm bảo tương thích ngược.

    Args:
        state: Trạng thái hiện tại của agent

    Returns:
        Trạng thái sau khi chuyển agent
    """
    return await router_node._switch_agent(state)
