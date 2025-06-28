from typing import Annotated,TypedDict, Sequence
from langchain_core.messages import BaseMessage
from langgraph.managed import IsLastStep, RemainingSteps
from langgraph.graph.message import add_messages

class AgentState(TypedDict):

    messages: Annotated[Sequence[BaseMessage], add_messages]

    is_last_step: IsLastStep
    
    remaining_steps: RemainingSteps
    
    agent_id: str

    configs: dict

    next: str
