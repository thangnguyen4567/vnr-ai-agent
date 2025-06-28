from .llm_handler import LLMHandler
from src.core import AgentState
from langchain_core.runnables import RunnableConfig

llm_handler = LLMHandler()
async def llm_call(state: AgentState, config: RunnableConfig):
    return await llm_handler.process(state, config)




