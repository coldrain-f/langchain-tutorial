import streamlit as st
import pandas as pd

from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
from typing import List, Dict


load_dotenv()


if "page_states" not in st.session_state:
    st.session_state["page_states"] = {}

if "few_shot_prompt_template" not in st.session_state["page_states"]:
    st.session_state["page_states"]["few_shot_prompt_template"] = {"messages": []}


def get_session_state() -> Dict:
    return st.session_state["page_states"]["few_shot_prompt_template"]


def add_message(role: str, message: str) -> None:
    session_state = get_session_state()
    messages: List[ChatMessage] = session_state["messages"]
    messages.append(ChatMessage(role=role, content=message))


def display_messages() -> None:
    messages: List[ChatMessage] = get_session_state()["messages"]
    for chat_message in messages:
        st.chat_message(chat_message.role).write(chat_message.content)


def create_chain():
    examples = [
        {
            "question": "문장이 긍정적인지 부정적인지 분류해주세요. #문장: 오늘은 날씨가 좋습니다.",
            "answer": "긍정",
        },
        {
            "question": "강아지 말투로 대답해주세요.",
            "answer": "알겠습니다. 야옹",
        },
    ]

    example_prompt = PromptTemplate.from_template(
        "Question:\n{question}\nAnswer:\n{answer}"
    )
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="Question:\n{question}\nAnswer:",
        input_variables=["question"],
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    chain = prompt | llm | StrOutputParser()
    return chain


with st.sidebar:
    st.title("LLM Lab")
    reset_button = st.button("Start new chat", type="tertiary")

    selected_shot = st.selectbox(
        "프롬프트 방식을 선택해주세요.", ("Zero Shot", "One Shot", "Few Shot"), index=0
    )

    with st.expander("Few Shot 예시"):
        st.json(
            [
                {
                    "question": "10 + 10은 어떤 문제입니까?",
                    "answer": "10 + 10은 덧셈 문제입니다.",
                },
                {
                    "question": "10 - 10은 어떤 문제입니까?",
                    "answer": "10 - 10은 뺄셈 문제입니다.",
                },
            ]
        )


if reset_button:
    session_state = get_session_state()
    session_state["messages"] = []


st.title("AI Assistant")
st.markdown(
    """
    **Zero Shot 프롬프팅:** LLM에게 예시를 제공하지 않고 그냥 질문
    
    **One Shot 프롬프팅:** LLM에게 예시를 1개 제공하여 질문
    
    **Few Shot 프롬프팅:** LLM에게 예시를 2개 이상 제공하여 질문
    """
)
st.divider()

user_message = st.chat_input()

display_messages()

if user_message:
    add_message("user", user_message)
    st.chat_message("user").write(user_message)

    chain = create_chain()
    chunks = chain.stream({"question": user_message})
    content = st.chat_message("assistant").write_stream(chunks)
    add_message("assistant", content)
