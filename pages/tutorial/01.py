import streamlit as st

from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from typing import List, Dict


load_dotenv()

if "page_states" not in st.session_state:
    st.session_state["page_states"] = {}

if "page_01" not in st.session_state["page_states"]:
    st.session_state["page_states"]["page_01"] = {"messages": []}


def get_session_state() -> Dict:
    return st.session_state["page_states"]["page_01"]


def add_message(role: str, message: str) -> None:
    session_state = get_session_state()
    messages: List[ChatMessage] = session_state["messages"]
    messages.append(ChatMessage(role=role, content=message))


def display_messages() -> None:
    messages: List[ChatMessage] = get_session_state()["messages"]
    for chat_message in messages:
        st.chat_message(chat_message.role).write(chat_message.content)


def generate_chat_completion(message: str, model: str):
    model = ChatOpenAI(model=model, temperature=0)
    return model.stream(message)


with st.sidebar:
    st.title("LLM Lab")
    reset_button = st.button("Start new chat", type="tertiary")
    selected_model = st.selectbox(
        "Please select an OpenAI model.", ("gpt-4o-mini", "gpt-4o")
    )


st.title("AI Assistant")
st.caption("LLM chatbot in its simplest form, without chains and RAG")
st.divider()

if reset_button:
    session_state = get_session_state()
    session_state["messages"] = []

display_messages()

user_message = st.chat_input()

if user_message:
    add_message("user", user_message)
    st.chat_message("user").write(user_message)

    chat_stream_completion = generate_chat_completion(user_message, selected_model)
    chat_completion = st.chat_message("assistant").write_stream(chat_stream_completion)
    add_message("assistant", chat_completion)
