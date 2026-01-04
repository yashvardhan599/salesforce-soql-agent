from langgraph.graph import END
from langgraph.types import Command
from langchain_core.messages import ToolMessage

from logger import logger
from runnables import agent_runnable
from state import SoqlState
from tools import agent_tools


def agent_node(state: SoqlState):
    logger.info(msg="Inside the Agent Node")

    response = agent_runnable.invoke({
        "messages": state["messages"],
        "table_info": state.get("table_info", {})
    })
    response.pretty_print()

    if response.tool_calls:
        if response.content:
            logger.debug(f"Tool Name: {response.tool_calls}")
            logger.info("Agent has tool calls as well as generated response")
        else:
            logger.info("Agent has tool calls but no generated response")

        return Command(
            update={
                "messages": state["messages"] + [response],
                "table_info": state.get("table_info", {})
            },
            goto="tool_node"
        )

    else:
        logger.info("- Agent has generated a response only")
        return Command(
            update={
                "messages": state["messages"] + [response],
                "table_info": state.get("table_info", {})
            },
            goto=END
        )
