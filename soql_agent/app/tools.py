import requests
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from state import SoqlState
from logger import logger
from prompts import QUERY_EXECUTOR_PROMPT
from llm import llm
from salesforce_auth import get_salesforce_token

@tool
def list_db_tables(state: Annotated[SoqlState, InjectedState]):
    access_token, instance_url = get_salesforce_token()

    url = f"{instance_url}/services/data/v59.0/sobjects/"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    tables = [obj["name"] for obj in response.json()["sobjects"]]

    return {
        "response": f"The tables available are: {tables}",
        "state": state
    }

@tool
def get_schema_of_table(table_names: list[str], state: Annotated[SoqlState, InjectedState]):
    access_token, instance_url = get_salesforce_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    result = {}

    for table in table_names:
        describe_url = f"{instance_url}/services/data/v59.0/sobjects/{table}/describe"
        describe_resp = requests.get(describe_url, headers=headers)
        describe_resp.raise_for_status()

        fields = [f["name"] for f in describe_resp.json().get("fields", [])]

        query = f"SELECT FIELDS(ALL) FROM {table} LIMIT 5"
        query_url = f"{instance_url}/services/data/v57.0/queryAll"
        rows_resp = requests.get(query_url, headers=headers, params={"q": query})
        rows = rows_resp.json().get("records", [])

        result[table] = {"schema": fields, "data": rows}

    state["table_info"] = result

    return {
        "response": str(result) + "\nSchema fetched. Proceed to query generation.",
        "state": state
    }


@tool
def soql_query_generator_and_executor(user_query: str, state: Annotated[SoqlState, InjectedState]):
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", QUERY_EXECUTOR_PROMPT),
        ("human", "{user_query}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "user_query": user_query,
        "messages": state["messages"],
        "table_info": state["table_info"]
    })

    return {"response": response, "state": state}

agent_tools = {
   "list_db_tables": list_db_tables,
   "get_schema_of_table": get_schema_of_table,
   "soql_query_generator_and_executor": soql_query_generator_and_executor
}