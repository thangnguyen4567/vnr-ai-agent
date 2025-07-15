from langgraph.graph import StateGraph, END
from src.core import AgentState
from src.core.nodes import initialize, router_agent, switch_agent, llm_aggregate_result
from IPython.display import Image
from langgraph.checkpoint.memory import InMemorySaver


class MultiAgent(StateGraph):

    def __init__(self):
        # Khởi tạo bộ nhớ đệm để lưu trạng thái của workflow theo thread_id
        memory = InMemorySaver()

        self.workflow = StateGraph(AgentState)

        self.workflow.add_node("initialize", initialize)
        self.workflow.add_node("router_agent", router_agent)
        self.workflow.add_node("switch_agent", switch_agent)
        self.workflow.add_node("llm_aggregate_result", llm_aggregate_result)

        # Khởi tạo trạng thái ban đầu , xử lý cấu hình agent và tạo các agent
        self.workflow.set_entry_point("initialize")
        # Router agent: chọn agent tiếp theo sẽ được chạy
        self.workflow.add_edge("initialize", "router_agent")
        # Switch agent: chuyển đổi agent và chạy agent được chọn chạy workflow fc_agent ( chạy song song nhiều agent)
        self.workflow.add_edge("router_agent", "switch_agent")
        # LLM aggregate result: tổng hợp kết quả từ các agent
        self.workflow.add_edge("switch_agent", "llm_aggregate_result")
        # Kết thúc workflow
        self.workflow.add_edge("llm_aggregate_result", END)

        self.compiled_graph = self.workflow.compile(checkpointer=memory)

    def get_graph(self):

        return self.compiled_graph

    def draw_workflow(self):
        Image(
            self.compiled_graph.get_graph().draw_mermaid_png(
                output_file_path="MultiAgent.png"
            )
        )


multi_agent_graph = MultiAgent().get_graph()
