import streamlit as st
import os

from typing import Annotated, List
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langchain_core.messages.chat import ChatMessage


if "messages" not in st.session_state:
    st.session_state["messages"] = []


# TypedDict를 상속 받아서 그래프 상태 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Tavily 도구 정의
tavily_search_tool = TavilySearchResults(
    max_results=3,
    include_domains=["github.io", "wikidocs.net"],
)

llm_tools = [tavily_search_tool]

# LLM 생성 및 도구 바인딩
llm = ChatOpenAI(model="gpt-4o-mini")

llm_with_tools = llm.bind_tools(llm_tools)


# LangGraph Chatbot 노드 정의
def chatbot(state: State):
    answer = llm_with_tools.invoke(state["messages"])
    return {"messages": [answer]}


# LangGraph Tools 노드 정의
tools = ToolNode(tools=[tavily_search_tool])

# LangGraph 노드 추가
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tools)

# LangGraph 간선 연결
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# LangGraph 조건부 간선 설정
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# LangGraph 컴파일
graph = graph_builder.compile()

# LangGraph 설정
config = RunnableConfig(recursion_limit=10)

with st.sidebar:
    st.title("LLM Lab")
    password = st.text_input("비밀번호", type="password")
    st.header("그래프 시각화")
    st.image(graph.get_graph().draw_mermaid_png())

st.title("AI Assistant")
st.divider()

messages: List[ChatMessage] = st.session_state["messages"]

for message in messages:
    st.chat_message(message.role).write(message.content)

user_message = st.chat_input()


if user_message:
    if password == os.getenv("PASSWORD"):
        st.chat_message("human").write(user_message)
        messages.append(ChatMessage(role="human", content=user_message))

        events = graph.stream({"messages": [user_message]})

        for event in events:
            for value in event.values():
                response_metadata = value["messages"][-1].response_metadata
                if "finish_reason" in response_metadata:
                    if response_metadata["finish_reason"] == "stop":
                        st.chat_message("assistant").write(
                            value["messages"][-1].content
                        )
                        messages.append(
                            ChatMessage(
                                role="assistant", content=value["messages"][-1].content
                            )
                        )
    else:
        st.error("비밀번호를 확인해 주세요.")
