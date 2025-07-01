from langgraph.graph import StateGraph
from src.core import AgentState
from src.core.nodes import initialize, llm_call, tool_call
from src.core.edges import route_llm_to_tool
from langgraph.graph import END
from IPython.display import Image
from src.memory.mongodb import get_mongodb_checkpointer


class FCAgent(StateGraph):

    def __init__(self):

        self.workflow = StateGraph(AgentState)

        self.workflow.add_node("initialize", initialize)
        self.workflow.add_node("llm", llm_call)
        self.workflow.add_node("tool", tool_call)

        self.workflow.set_entry_point("initialize")

        self.workflow.add_conditional_edges(
            "llm", route_llm_to_tool, {"continue": "tool", "end": END}
        )

        self.workflow.add_edge("tool", "llm")
        self.workflow.add_edge("initialize", "llm")

        # Sử dụng MongoDB checkpointer
        # mongodb_saver = get_mongodb_checkpointer()

        self.compiled_graph = self.workflow.compile()

    def get_graph(self):

        return self.compiled_graph

    def draw_workflow(self):
        Image(
            self.compiled_graph.get_graph().draw_mermaid_png(
                output_file_path="fc_agent_workflow.png"
            )
        )


fc_agent_graph = FCAgent().get_graph()
