from src.core.nodes.base_node import BaseNode
from src.core import AgentState
from langchain_core.runnables import RunnableConfig
from typing import Dict, Any
from langchain_openai import ChatOpenAI
import copy
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from dotenv import load_dotenv
from src.config import settings
import logging
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import JsonOutputParser
import asyncio
from src.prompt import ROUTER_AGENT_PROMPT, PREFIX_AGENT_KEY, AGENT_DESC_TEMPLATE
load_dotenv()

class AgentList(BaseModel):
    agents: List[str]
    
class RouterNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.llm_router_agent = ChatOpenAI(
            base_url=settings.LLM_CONFIG["router"]["base_url"],
            model=settings.LLM_CONFIG["router"]["model"],
            temperature=settings.LLM_CONFIG["router"]["temperature"],
            stream_usage=True,
            api_key=settings.LLM_CONFIG["router"]["api_key"],
            max_tokens=20,
        )

    async def process(
        self, state: AgentState, config: RunnableConfig
    ) -> Dict[str, Any]:

        routing_result = await self._router_agent(state, config)

        state["next"] = routing_result["next"]
        state["agent_id"] = routing_result["agent_id"]

        return await self._switch_agent(state)

    def _router_agent(
        self, state: AgentState, config: RunnableConfig
    ) -> Dict[str, Any]:
        """
        Phân tích cuộc hội thoại và xác định agent phù hợp

        Args:
            state: Trạng thái hiện tại của agent
            config: Cấu hình của agent

        Returns:
            Kết quả routing với agent tiếp theo
        """
        # Lấy cấu hình từ cấu hình xml
        sys_config = config.get("configurable", {})
        agent_id = sys_config.get("agent_id")
        agent_config = state.get("configs", {}).get(agent_id, {})
        agents = agent_config.get("agents", [])
        default_agent = copy.deepcopy(agents[0])

        # Lấy thông tin các agent từ cấu hình xml
        agent_desc = []
        agent_keys = []
        subgraph_mapping = {}
        for i, a in enumerate(agents):
            _key = f"{PREFIX_AGENT_KEY}{i+1}"
            agent_keys.append(_key)
            agent_desc.append(
                AGENT_DESC_TEMPLATE.format(
                    agent_key=_key,
                    agent_name=a["name"],
                    agent_description=a["description"],
                )
            )
            subgraph_mapping[_key] = {"code": a["code"], "id": a["agent_id"]}
        agent_desc_str = "\n".join(agent_desc)

        messages = []
        for msg in state["messages"]:
            if isinstance(msg, AIMessage) and msg.content:
                messages.append(f"assistant: {msg.content}")
            elif isinstance(msg, HumanMessage) and msg.content:
                messages.append(f"user: {msg.content}")

        parser = JsonOutputParser(pydantic_object=AgentList)
        new_messages = [
            (
                "human",
                ROUTER_AGENT_PROMPT.format(
                    agent_keys=str(agent_keys),
                    agent_desc=agent_desc_str,
                    chat_history="\n".join(messages[-4:]),
                    format_instructions=parser.get_format_instructions()
                ),
            )
        ]

        chain = self.llm_router_agent | parser
        res = chain.invoke(new_messages)

        try:
            next_agent = []
            agent_id = []

            for k, v in subgraph_mapping.items():
                if k in res['agents']:
                    next_agent.append(k)

            goto = [subgraph_mapping[k]["code"] for k in next_agent]
            agent_id = [subgraph_mapping[k]["id"] for k in next_agent]
        except:
            goto = default_agent["code"]
            agent_id = default_agent["id"]

        return {"next": goto, "agent_id": agent_id}

    async def _switch_agent(self, state: AgentState):
        """
        Chuyển sang agent được chỉ định và xử lý hội thoại

        Args:
            state: Trạng thái hiện tại của agent_id và next đã được cập nhật

        Returns:
            Trạng thái mới sau khi xử lý
        """

        from src.core.fc_agent import fc_agent_graph

        tasks = []
        next_agent = state["next"]
        node_state = state.copy()
        node_state["messages"] = []
        new_messages = []

        for msg in state["messages"]:
            if (
                isinstance(msg, AIMessage)
                and not msg.content
                and msg.name != next_agent
            ):
                continue
            if isinstance(msg, ToolMessage) and msg.name != next_agent:
                continue
            node_state["messages"].append(msg)

        for agent_id in state["agent_id"]:
            # clone node_state cho từng agent để tránh ghi đè
            node_state = dict(state)
            node_state["agent_id"] = agent_id
            task = fc_agent_graph.ainvoke(node_state)
            tasks.append(task)
        # chờ tất cả các task hoàn thành ( các task có thể chạy song song)
        results = await asyncio.gather(*tasks)

        for result in results:
            new_messages.extend(result["messages"][len(node_state["messages"]) :])

        # Cập nhật trạng thái với message mới
        new_state = state.copy()
        new_state["messages"] = state["messages"]

        for msg in new_messages:
            new_state["messages"].append(msg)

        return new_state