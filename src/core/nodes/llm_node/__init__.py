from .llm_handler import LLMHandler
from .llm_ui_handler import LLMUIHandler
from src.core import AgentState
from langchain_core.runnables import RunnableConfig

llm_handler = LLMHandler()
llm_ui_handler = LLMUIHandler()

async def llm_call(state: AgentState, config: RunnableConfig):
    return await llm_handler.process(state, config)

async def llm_ui_action(state: AgentState, config: RunnableConfig):
    return await llm_ui_handler.process(state, config)