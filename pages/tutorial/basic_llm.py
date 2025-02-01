import streamlit as st
import pandas as pd

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


with st.sidebar:
    st.title("LLM Lab")
    reset_button = st.button("Start new chat", type="tertiary")
    selected_model = st.selectbox(
        "Please select an OpenAI model.", ("gpt-4o-mini", "gpt-4o"), index=0
    )

    selected_output_type = st.selectbox(
        "Please select an Output type.", ("Stream", "Invoke"), index=0
    )


data = {
    "PROMPT": [None],
    "LOADER": [None],
    "OUTPUT PARSER": [None],
    "MODEL": [selected_model],
    "CHAIN": [None],
}
df = pd.DataFrame(data)

st.title("AI Assistant")
st.dataframe(df, use_container_width=True)
st.divider()

if reset_button:
    session_state = get_session_state()
    session_state["messages"] = []

display_messages()

user_message = st.chat_input()

if user_message:
    add_message("user", user_message)
    st.chat_message("user").write(user_message)

    model = ChatOpenAI(model=selected_model, temperature=0)
    if selected_output_type == "Stream":
        response = model.stream(user_message)
        content = st.chat_message("assistant").write_stream(response)
        add_message("assistant", content)
    elif selected_output_type == "Invoke":
        response = model.invoke(user_message)
        st.chat_message("assistant").write(response.content)
        add_message("assistant", response.content)
