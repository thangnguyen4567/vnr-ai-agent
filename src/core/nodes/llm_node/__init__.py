from .llm_handler import LLMHandler
from .llm_ui_handler import LLMUIHandler
from src.core import AgentState
from langchain_core.runnables import RunnableConfig

llm_handler = LLMHandler()
llm_ui_handler = LLMUIHandler()

def llm_call(state: AgentState, config: RunnableConfig):
    return llm_handler.process(state, config)

def llm_ui_action(state: AgentState, config: RunnableConfig):
    return llm_ui_handler.process(state, config)