from langgraph.graph import StateGraph
from src.core import AgentState
from src.core.nodes import initialize, llm_call, tool_call
from src.core.edges import route_llm_to_tool
from langgraph.graph import END
from IPython.display import Image
from langgraph.checkpoint.memory import InMemorySaver


class FCAgent(StateGraph):
    """
    Sub workflow của multi agent được gọi ở node switch agent
    """
    def __init__(self):
        self.workflow = StateGraph(AgentState)
        # Khởi tạo trạng thái ban đầu
        self.workflow.add_node("initialize", initialize)
        # Gọi LLM để xử lý tin nhắn người dùng và trả về kết quả của tool call
        self.workflow.add_node("llm", llm_call)
        # Gọi tool để lấy dữ liệu từ bên ngoài
        self.workflow.add_node("tool", tool_call)

        self.workflow.set_entry_point("initialize")

        self.workflow.add_conditional_edges(
            "llm", 
            route_llm_to_tool, 
            {
                "continue": "tool", 
                "end": END
            }
        )

        self.workflow.add_edge("initialize", "llm")
        
        # Khởi tạo bộ nhớ đệm để lưu trạng thái của workflow theo thread_id
        memory = InMemorySaver()

        # Compile workflow
        self.compiled_graph = self.workflow.compile(checkpointer=memory)

    def get_graph(self):

        return self.compiled_graph

    def draw_workflow(self):
        Image(
            self.compiled_graph.get_graph().draw_mermaid_png(
                output_file_path="fc_agent_workflow.png"
            )
        )


fc_agent_graph = FCAgent().get_graph()
