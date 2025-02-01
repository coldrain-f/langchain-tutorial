import streamlit as st
import pandas as pd
import os

from dotenv import load_dotenv
from typing import List, Dict, Any

from langchain_core.documents.base import Document
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages.chat import ChatMessage
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableSerializable

# Chain은 처음 전처리할 때 한 번만 만들어두고,
# 그 다음부터는 사용자가 질문할 때마다 같은 Chain을 활용하면 된다.

load_dotenv()

if not os.path.exists(".cache"):
    os.mkdir(".cache")

if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")

if "page_states" not in st.session_state:
    st.session_state["page_states"] = {}

if "page_02" not in st.session_state["page_states"]:
    st.session_state["page_states"]["page_02"] = {"messages": [], "chain": None}


def get_session_state():
    return st.session_state["page_states"]["page_02"]


def add_message(role: str, message: str) -> None:
    session_state = get_session_state()
    messages: List[ChatMessage] = session_state["messages"]
    messages.append(ChatMessage(role=role, content=message))


def display_messages() -> None:
    messages: List[ChatMessage] = get_session_state()["messages"]
    for chat_message in messages:
        st.chat_message(chat_message.role).write(chat_message.content)


@st.cache_resource(show_spinner="Processing the file that you uploaded.")
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    # PDF 불러오기
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    # 청크 단위로 분할하기
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(documents)

    # 임베딩 하기
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(split_documents, embedding=embeddings)

    retriever = vector_store.as_retriever()
    return retriever


def create_chain(
    model_name: str, retriever: BaseRetriever
) -> RunnableSerializable[Any, str]:
    prompt = PromptTemplate.from_template(
        """You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Please write your answer in a markdown table format with the main points.
    Be sure to include your source and page numbers in your answer.
    Answer in Korean.

    #Example Format:
    (brief summary of the answer)
    (answer to the question)
    (table)
    
    **출처**
    - page source and page number
    
    #Question : {question}

    #Context: {context}
    
    #Answer:"""
    )

    model = ChatOpenAI(model=model_name, temperature=0)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain


with st.sidebar:
    st.title("LLM Lab")
    reset_button = st.button("Start new chat", type="tertiary")

    st.subheader("Options")
    selected_model = st.selectbox(
        "Please select an OpenAI model.", ("gpt-4o-mini", "gpt-4o")
    )
    uploaded_files = st.file_uploader("Choose a file", type=["pdf"])


data = {
    "PROMPT": ["PromptTemplate"],
    "LOADER": ["PyMuPDFLoader"],
    "OUTPUT PARSER": ["StrOutputParser"],
    "MODEL": [selected_model],
    "CHAIN": [True],
}
df = pd.DataFrame(data)

st.title("AI Assistant")
st.dataframe(df, use_container_width=True)
st.divider()

if uploaded_files:
    retriever = embed_file(uploaded_files)
    session_state = get_session_state()
    session_state["chain"] = create_chain(selected_model, retriever)
    st.write("Chain 생성")


if reset_button:
    session_state = get_session_state()
    session_state["messages"] = []

display_messages()

user_message = st.chat_input()

if user_message:

    session_state = get_session_state()
    chain: RunnableSerializable[Any, str] = session_state["chain"]

    if chain is None:
        st.error("Please upload a PDF file.")

    else:
        st.chat_message("user").write(user_message)
        add_message("user", user_message)

        chat_stream_completion = chain.stream(user_message)
        chat_completion = st.chat_message("assistant").write_stream(
            chat_stream_completion
        )
        add_message("assistant", chat_completion)
