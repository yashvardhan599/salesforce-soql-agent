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


agent_tools = {
   "list_db_tables": list_db_tables
}