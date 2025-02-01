import streamlit as st
import pandas as pd

from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnableSerializable
from langchain_core.prompts import load_prompt

from dotenv import load_dotenv
from typing import List, Dict


load_dotenv()

if "page_states" not in st.session_state:
    st.session_state["page_states"] = {}

if "basic_llm_use_chain" not in st.session_state["page_states"]:
    st.session_state["page_states"]["basic_llm_use_chain"] = {
        "messages": [],
        "chain": None,
    }


def get_session_state() -> Dict:
    return st.session_state["page_states"]["basic_llm_use_chain"]


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

    st.subheader("Options")
    selected_model = st.selectbox(
        "Please select an OpenAI model.", ("gpt-4o-mini", "gpt-4o"), index=0
    )

    selected_output_type = st.selectbox(
        "Please select an Output type.", ("Stream", "Invoke"), index=0
    )

    st.subheader("Template")
    st.code(
        """_type: "prompt"
template: "Make it easy to answer questions. #Question: {question}"
input_variables: ["question"]""",
        "yaml",
    )


data = {
    "PROMPT": ["PromptTemplate"],
    "LOADER": [None],
    "OUTPUT PARSER": ["StrOutputParser"],
    "MODEL": [selected_model],
    "CHAIN": [True],
}
df = pd.DataFrame(data)

st.title("AI Assistant")
st.dataframe(df, use_container_width=True)
st.divider()

if reset_button:
    session_state = get_session_state()
    session_state["messages"] = []

display_messages()

# Chain 구성
session_state = get_session_state()
if session_state["chain"] is None:
    with st.spinner():
        # 프롬프트 파일 불러오기
        prompt = load_prompt("./prompts/basic.yaml")
        model = ChatOpenAI(model=selected_model, temperature=0)

        chain: RunnableSerializable[dict, str] = prompt | model | StrOutputParser()
        session_state["chain"] = chain

user_message = st.chat_input()

if user_message:
    add_message("user", user_message)
    st.chat_message("user").write(user_message)

    chain = session_state["chain"]
    if selected_output_type == "Stream":
        message_chunk = chain.stream({"question": user_message})
        content = st.chat_message("assistant").write_stream(message_chunk)
        add_message("assistant", content)
    elif selected_output_type == "Invoke":
        content = chain.invoke({"question": user_message})
        st.chat_message("assistant").write(content)
        add_message("assistant", content)
