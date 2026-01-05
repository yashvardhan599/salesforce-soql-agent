import streamlit as st
from uuid import uuid4

from graph import SoqlGraph
from state import SoqlState
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="SOQL Agent", layout="wide")

st.title("🤖 Salesforce SOQL Agent")

if "graph" not in st.session_state:
    st.session_state.graph = SoqlGraph().build_graph().graph
    st.session_state.state = SoqlState(messages=[], table_info={})
    st.session_state.thread_id = uuid4()

config = {"configurable": {"thread_id": st.session_state.thread_id}}

user_input = st.chat_input("Ask your SOQL question...")

if user_input:
    st.session_state.state["messages"].append(HumanMessage(content=user_input))

    result_state = st.session_state.graph.invoke(
        st.session_state.state,
        config=config
    )

    st.session_state.state = result_state

for msg in st.session_state.state["messages"]:
    if hasattr(msg, "content"):
        st.chat_message("assistant").write(msg.content)
