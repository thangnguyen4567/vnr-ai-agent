from src.core import AgentState
from langchain_core.messages import AIMessage

def route_llm_to_tool(state: AgentState):

    if not state["messages"]:
        return "end"
    
    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls"):
        # return continue thì sẽ forward tới tool node chuyên xử lý tool call
        return "continue" if last_message.tool_calls else "end"
    else:
        # nếu không có tool call thì sẽ kết thúc agent
        return "end"


