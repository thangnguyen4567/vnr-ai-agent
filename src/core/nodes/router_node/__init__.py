from .supervisor import RouterNode
from src.core import AgentState
from langchain_core.runnables import RunnableConfig

router_node = RouterNode()
async def router_agent(state: AgentState, config: RunnableConfig):
    return router_node._router_agent(state, config)


async def switch_agent(state: AgentState):
    return await router_node._switch_agent(state)
