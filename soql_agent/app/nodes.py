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


def tool_node(state: SoqlState):
    logger.info(msg="Inside the Tool Node")

    tool_calls = state.get("messages", [])[-1].tool_calls

    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"].copy()
        tool_call_id = tool_call["id"]

        logger.info(msg=f"@tool args `{tool_args}`")
        logger.debug(f"Invoking tool: {tool_name} with args: {tool_args}")

        tool = agent_tools[tool_name]
        updated_tool_call_args = {**tool_args, "state": state}

        tool_result = tool.invoke(updated_tool_call_args)

        state.update(tool_result.get("state", {}))

        # if "state" in tool_result:
        #     state.update(tool_result["state"])

        state["messages"] = state["messages"] + [
            ToolMessage(
                content=str(tool_result["response"]),
                tool_call_id=tool_call_id
            )
        ]

    table_info = state.get("table_info", {})

    return Command(
        update={
            "messages": state["messages"],
            "table_info": table_info
        },
        goto="agent_node"
    )