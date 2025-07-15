from .llm_handler import LLMHandler
from src.core import AgentState
from langchain_core.runnables import RunnableConfig

llm_handler = LLMHandler()
async def llm_call(state: AgentState, config: RunnableConfig):
    return await llm_handler.process(state, config)


async def llm_aggregate_result(state: AgentState, config: RunnableConfig):
    return await llm_handler.aggregate_result(state, config)

