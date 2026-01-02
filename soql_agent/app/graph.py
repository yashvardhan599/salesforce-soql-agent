from nodes import agent_node, tool_node
from state import SoqlState
from logger import logger

from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import InMemorySaver


class SoqlGraph:
    def __init__(self):
        self.graph = None

    def build_graph(self) -> 'SoqlGraph':
        logger.info(msg="Building the SOQL Graph")

        builder = StateGraph(SoqlState)
        builder.add_node("agent_node", agent_node)
        builder.add_node("tool_node", tool_node)

        builder.add_edge(START, "agent_node")

        self.graph = builder.compile(checkpointer=InMemorySaver())

        return self