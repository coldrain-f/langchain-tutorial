import streamlit as st

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()


# 상태 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 노드 정의
def chatbot(state: State):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = state["messages"]
    return {"messages": llm.invoke(messages)}


# 그래프 생성
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

# 간선 연결
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# 그래프 컴파일
graph = graph_builder.compile()

st.header("LangGraph 기본 구조 확인")
start_button = st.button("실행")

if start_button:
    with st.expander("노드 1개와 메시지 1개인 구조"):
        st.subheader("Graph 이벤트 출력")
        for event in graph.stream(
            {"messages": [{"role": "human", "content": "대한민국의 수도는?"}]}
        ):
            st.write(event.values())

        st.subheader("Graph 이벤트 값 출력")
        for event in graph.stream(
            {"messages": [{"role": "human", "content": "대한민국의 수도는?"}]}
        ):
            for value in event.values():
                st.write(value)

        st.subheader("Graph 이벤트 값의 메시지 출력")
        for event in graph.stream(
            {"messages": [{"role": "human", "content": "대한민국의 수도는?"}]}
        ):
            for value in event.values():
                st.write(value["messages"])

        st.subheader("Graph 이벤트 값의 메시지의 내용 출력")
        for event in graph.stream(
            {"messages": [{"role": "human", "content": "대한민국의 수도는?"}]}
        ):
            for value in event.values():
                st.chat_message("assistant").write(value["messages"].content)
