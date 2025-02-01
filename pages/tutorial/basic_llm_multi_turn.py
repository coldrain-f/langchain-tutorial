import streamlit as st
import pandas as pd

from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

from dotenv import load_dotenv
from typing import List

load_dotenv()

if "page_states" not in st.session_state:
    st.session_state["page_states"] = {}

if "basic_llm_multi_turn" not in st.session_state["page_states"]:
    st.session_state["page_states"]["basic_llm_multi_turn"] = {
        "messages": [],
        "store": {},
        "chain_with_history": None,
    }


def get_session_state():
    return st.session_state["page_states"]["basic_llm_multi_turn"]


def add_message(role: str, message: str) -> None:
    session_state = get_session_state()
    messages: List[ChatMessage] = session_state["messages"]
    messages.append(ChatMessage(role=role, content=message))


def display_messages() -> None:
    messages: List[ChatMessage] = get_session_state()["messages"]
    for message in messages:
        st.chat_message(message.role).write(message.content)


def get_session_history(session_id):
    store = get_session_state()["store"]
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def create_chain_with_history():
    template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an assistant for question-answering tasks."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    chain = template | model | StrOutputParser()

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    return chain_with_history


with st.sidebar:
    st.title("LLM Lab")
    reset_button = st.button("Start new chat", type="tertiary")

    st.subheader("Options")
    selected_model = st.selectbox(
        "Please select an OpenAI model.", ("gpt-4o-mini", "gpt-4o"), index=0
    )

data = {
    "PROMPT": ["ChatPromptTemplate"],
    "LOADER": [None],
    "OUTPUT PARSER": ["StrOutputParser"],
    "MODEL": [selected_model],
    "MEMORY": [None],
    "CHAIN": [True],
}
df = pd.DataFrame(data)

if reset_button:
    st.session_state["page_states"]["basic_llm_multi_turn"] = {
        "messages": [],
        "store": {},
        "chain_with_history": None,
    }

st.title("AI Assistant")
st.dataframe(df, use_container_width=True)
st.divider()

display_messages()

# 한 번만 만들어서 재활용
session_state = get_session_state()

chain_with_history = session_state["chain_with_history"]
if chain_with_history is None:
    chain_with_history = create_chain_with_history()
    session_state["chain_with_history"] = chain_with_history

user_message = st.chat_input()

if user_message:
    add_message("human", user_message)
    st.chat_message("human").write(user_message)

    message_chunk = chain_with_history.stream(
        {"question": user_message},
        config={
            "configurable": {"session_id": "Woon"},
        },
    )

    content = st.chat_message("assistant").write_stream(message_chunk)
    add_message("assistant", content)
