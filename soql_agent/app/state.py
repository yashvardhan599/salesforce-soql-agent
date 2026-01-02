from typing import List

from typing_extensions import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class SoqlState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    table_info: dict