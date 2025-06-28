from langgraph.graph import StateGraph, END
from src.core import AgentState
from src.core.nodes import initialize, router_agent, switch_agent
from IPython.display import Image

class MultiAgent(StateGraph):

    def __init__(self):

        self.workflow = StateGraph(AgentState)

        self.workflow.add_node("initialize", initialize)
        self.workflow.add_node("router_agent", router_agent)
        self.workflow.add_node("switch_agent", switch_agent)

        self.workflow.set_entry_point("initialize")

        self.workflow.add_edge("initialize", "router_agent")
        self.workflow.add_edge("router_agent", "switch_agent")

        self.compiled_graph = self.workflow.compile()

    def get_graph(self):

        return self.compiled_graph
    
    def draw_workflow(self):
        Image(self.compiled_graph.get_graph().draw_mermaid_png(output_file_path='MultiAgent.png'))


multi_agent_graph = MultiAgent().get_graph()
# MultiAgent().draw_workflow()





