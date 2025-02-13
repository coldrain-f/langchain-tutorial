import streamlit as st

from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI

from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv
from typing import List, Dict


load_dotenv()

if "page_states" not in st.session_state:
    st.session_state["page_states"] = {}

if "tavily_llm" not in st.session_state["page_states"]:
    st.session_state["page_states"]["tavily_llm"] = {"messages": []}


def get_session_state() -> Dict:
    return st.session_state["page_states"]["tavily_llm"]


def add_message(role: str, message: str) -> None:
    session_state = get_session_state()
    messages: List[ChatMessage] = session_state["messages"]
    messages.append(ChatMessage(role=role, content=message))


def display_messages() -> None:
    messages: List[ChatMessage] = get_session_state()["messages"]
    for chat_message in messages:
        st.chat_message(chat_message.role).write(chat_message.content)


with st.sidebar:
    st.title("LLM Lab")
    reset_button = st.button("Start new chat", type="tertiary")


st.title("AI Assistant")
st.divider()

if reset_button:
    session_state = get_session_state()
    session_state["messages"] = []

user_message = st.chat_input()

display_messages()

tavily_search_tool = TavilySearchResults(
    max_results=5,
    include_answer=True,
    include_raw_content=True,
    include_domains=["https://ko.wikipedia.org/wiki"],
)

if user_message:
    add_message("user", user_message)
    st.chat_message("user").write(user_message)

    search_results = tavily_search_tool.invoke(user_message)
    ai_message = ""
    index = 0
    for search_result in search_results:
        index += 1
        ai_message += f"""
##### 검색 결과 - {index}

{search_result["content"]}

[링크 바로가기]({search_result["url"]})\n\n
"""
    st.chat_message("assistant").write(ai_message)
    add_message("assistant", ai_message)
