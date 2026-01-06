from llm import llm
# from tools import Tools
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import list_db_tables, get_schema_of_table, soql_query_generator_and_executor
from prompts import AGENT_PROMPT
from logger import logger


def get_agent_runnable():
    logger.info("Inside the Agent Runnable")
    agent_prompt_template = ChatPromptTemplate.from_messages([
        ("system", AGENT_PROMPT),
        MessagesPlaceholder("messages")]
    )

    agent_runnable = RunnableSequence(
        agent_prompt_template,
        llm.bind_tools([list_db_tables, get_schema_of_table, soql_query_generator_and_executor])
    )

    logger.info("Agent Runnable Build")

    return agent_runnable


agent_runnable = get_agent_runnable()

