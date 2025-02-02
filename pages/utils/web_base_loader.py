import streamlit as st
import pandas as pd
import requests
import json

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from bs4 import BeautifulSoup


if "session" not in st.session_state:
    st.session_state["session"] = None

if not st.session_state["session"]:
    st.session_state["session"] = requests.session()


st.title("JPDB Web Crawling")
st.subheader("JSON Viewer")
json_file_to_display = st.file_uploader(
    "Please choose the JSON file to display.", type=["json"]
)
if json_file_to_display:
    df = pd.DataFrame(json.load(json_file_to_display))
    st.data_editor(df, use_container_width=True)

st.subheader("Meaning Generator")
st.caption("Format")
st.json(
    [
        {"Frequency": 1, "Expression": "する", "Reading": "", "Meaning": ""},
    ]
)
json_file_for_meaning = st.file_uploader(
    "Choose a file to generate meanings", type=["json"]
)

if json_file_for_meaning:
    generate_button = st.button("Generate")
    if generate_button:
        json_file = json.load(json_file_for_meaning)
        template = PromptTemplate.from_template(
            """ You are a teacher of Korean and Japanese with 20 years' experience.
            Look at this #Expression and write its meaning in Korean short answer. 
            No explanation is needed.
            
            #Expression: {expression}"""
        )

        model = ChatOpenAI(model="gpt-4o", temperature=0)
        chain = template | model | StrOutputParser()

        # 프로그레스바 생성
        progress_text = "Operation in progress. Please wait."
        generator_progress_bar = st.progress(0, text=progress_text)

        index = 0
        newWords = []
        for json_data in json_file:
            if index >= 26220:
                break

            input = {"expression": json_data["Expression"]}
            meaning = chain.invoke(input)
            words = {
                "Frequency": json_data["Frequency"],
                "Expression": json_data["Expression"],
                "Reading": "",
                "Meaning": meaning,
            }
            newWords.append(words)
            index += 1
            generator_progress_bar.progress(
                int((index / 26220) * 100), text=progress_text
            )

        st.download_button(
            label="Download New JSON",
            file_name="new_data.json",
            mime="application/json",
            data=json.dumps(newWords, ensure_ascii=False, indent=2),
        )

st.subheader("Crawling")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
begin = st.number_input("Begin", value=0)
end = st.number_input("End", value=0)

submit_button = st.button("Submit")


if submit_button:
    # 아이디 또는 비밀번호를 입력하지 않았을 경우 에러 메시지 출력.
    if not username or not password:
        st.error("Please enter your Username and Password")
    else:
        # JPDB를 파싱하여 50개씩 단어를 뽑아낸다.
        with st.spinner():
            login_info = {
                "username": username,
                "password": password,
            }
            login_url = "https://jpdb.io/login"
            st.session_state["session"].post(login_url, data=login_info)

            frequency = 1
            words = []
            for offset in range(begin, end, 50):
                response = st.session_state["session"].get(
                    f"https://jpdb.io/deck?id=6&offset={offset}"
                )
                response.encoding = "utf-8"

                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                vocabulary_list = soup.select("div.entry")

                for vocabulary in vocabulary_list:
                    a = vocabulary.select_one("div.vocabulary-spelling > a")
                    words.append(
                        {
                            "Frequency": frequency,
                            "Expression": a.text,
                            "Reading": "",
                            "Meaning": "",
                        }
                    )
                    frequency += 1

        st.download_button(
            label="Download JSON",
            file_name="data.json",
            mime="application/json",
            data=json.dumps(words, ensure_ascii=False, indent=2),
        )
