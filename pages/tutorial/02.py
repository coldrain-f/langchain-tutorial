import streamlit as st

from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from typing import List


load_dotenv()

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def add_message(role: str, message: str) -> None:
    messages = st.session_state["messages"]
    messages.append(ChatMessage(role=role, content=message))


def display_messages() -> None:
    messages: List[ChatMessage] = st.session_state["messages"]
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
    st.session_state["messages"] = []

display_messages()

user_message = st.chat_input()

if user_message:
    add_message("user", user_message)
    st.chat_message("user").write(user_message)

    chat_stream_completion = generate_chat_completion(user_message, selected_model)
    chat_completion = st.chat_message("assistant").write_stream(chat_stream_completion)
    add_message("assistant", chat_completion)
