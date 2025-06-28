from .init_agent_context import ContextInitializer
from src.core import AgentState
from langchain_core.runnables import RunnableConfig

context_initializer = ContextInitializer()
async def initialize(state: AgentState, config: RunnableConfig) -> AgentState:
    return await context_initializer.process(state, config)




