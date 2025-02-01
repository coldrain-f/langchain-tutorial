import streamlit as st

from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

with st.sidebar:
    st.title("LLM Lab")

with st.spinner():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

st.header("LangChain")

st.subheader("langchain_core.messages.chat")
with st.expander("ChatMessage"):
    st.write(ChatMessage(role="human", content="Hello World!"))

st.subheader("langchain_openai")
with st.expander("ChatOpenAI"):
    st.json(model, expanded=2)

with st.expander("ChatOpenAI - stream()"):
    question = "대한민국의 수도는?"
    message_chunk = model.stream(question)

    st.code(
        """model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
question = "대한민국의 수도는?"
message_chunk = model.stream(question)
        
for chunk in message_chunk:
    st.json(chunk)
""",
        "python",
    )
    for chunk in message_chunk:
        st.json(chunk)
