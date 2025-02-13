import streamlit as st

from typing import Annotated, List, Dict
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages.chat import ChatMessage

from dotenv import load_dotenv

load_dotenv()

if "page_states" not in st.session_state:
    st.session_state["page_states"] = {}

if "basic_llm_langgraph_chatbot" not in st.session_state["page_states"]:
    st.session_state["page_states"]["basic_llm_langgraph_chatbot"] = {
        "messages": [],
        "graph": None,
    }


def get_session_state() -> Dict:
    return st.session_state["page_states"]["basic_llm_langgraph_chatbot"]


def add_message(role: str, message: str) -> None:
    session_state = get_session_state()
    messages: List[ChatMessage] = session_state["messages"]
    messages.append(ChatMessage(role=role, content=message))


def display_messages() -> None:
    messages: List[ChatMessage] = get_session_state()["messages"]
    for chat_message in messages:
        st.chat_message(chat_message.role).write(chat_message.content)


# LangGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]


def call_llm(state: State):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = state["messages"]
    return {"messages": [llm.invoke(messages)]}


def build_state_graph():
    graph_builder = StateGraph(State)

    graph_builder.add_node("call_llm", call_llm)

    graph_builder.add_edge(START, "call_llm")
    graph_builder.add_edge("call_llm", END)

    graph = graph_builder.compile()
    return graph


graph = get_session_state()["graph"]
if graph is None:
    graph = build_state_graph()

with st.sidebar:
    st.title("LLM Lab")
    reset_button = st.button("Start new chat", type="tertiary")
    st.header("시각화")
    st.image(graph.get_graph().draw_mermaid_png())

st.title("AI Assistant")
st.markdown(
    """Graph 상태에 add_messages 리듀서를 사용 중인데 메시지가 누적되지 않는 문제가 있음...
    
개념을 더 익히고 왜 그런지 문제 파악 필요."""
)
st.divider()

if reset_button:
    session_state = get_session_state()
    session_state["messages"] = []

user_message = st.chat_input()

display_messages()

if user_message:
    add_message("human", user_message)
    st.chat_message("human").write(user_message)

    for event in graph.stream(
        {"messages": [{"role": "human", "content": user_message}]}
    ):
        for value in event.values():
            content = value["messages"][-1].content
            st.chat_message("assistant").write(content)
            add_message("assistant", content)
