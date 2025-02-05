import streamlit as st
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# https://ja.dict.naver.com/#/search?range=all&query={expression}

st.title("Naver Dict Web Crawling")
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

        # 1개만 가지고 테스트
        expression = json_file[36]["Expression"]

        # 브라우저 자동 닫힘 방지
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", False)
        driver = webdriver.Chrome(options=chrome_options)

        # 브라우저 열기
        # driver.get(f"https://ja.dict.naver.com/#/search?range=all&query={expression}")
        driver.get(f"https://dic.daum.net/search.do?q={expression}")

        # 필요한 요소가 로드될 때까지 대기
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.fold_ex"))
        )
        html = """
            <style>
                @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-jp.min.css");

                    * {
                        font-family: "Pretendard JP";
                    }

                    a {
                        color: #000;
                        text-decoration: none;
                    }
                    .container {
                        background-color: white;
                        padding: 30;
                    }

                    /** 동의어 시작 **/
                    .ex_refer {
                        display: block;
                        position: relative;
                        overflow: hidden;
                        margin: 10px 0 13px 0;
                        padding: 10px 29px 10px 29px;
                        border: 1px solid #ececec;
                        border-radius: 3px;
                    }

                    .ex_refer dt {
                        float: left;
                        padding-right: 10px;
                        font-size: 15px;
                    }

                    .txt_emph3 {
                        color: #688ab3;
                    }
                    .ex_refer .link_refer {
                        float: left;
                        font-size: 15px;
                        color: #666;
                    }

                    .ex_refer .link_refer:hover {
                        text-decoration: underline;
                    }

                    /** 동의어 끝 **/
                    .ruby {
                        color: #f95460;
                        font-size: 12px;
                    }
                    .wrap_ex,
                    .desc_item {
                        padding: 0;
                        margin: 0;
                        display: inline-block;
                        line-height: 27px;
                    }

                    .wrap_ex {
                        font-size: 17px;
                        font-weight: 500;
                    }

                    .item_example {
                        display: block;
                        position: relative;
                        margin: 8px 0 0 30px;
                        padding-left: 15px;
                        border-left: 2px solid #ededed;
                        line-height: 20px;
                        font-size: 15px;
                    }

                    p.desc_ruby {
                        margin-top: 0;
                        margin-bottom: 0;
                    }

                    p.desc_ex {
                        color: #888;
                        font-weight: 500;
                    }

                    dl,
                    ul,
                    ol,
                    menu,
                    li {
                        list-style: none;
                    }
            </style>
        """
        html += f"""
            {element.get_attribute("innerHTML")}
        """
        st.html(html)

        st.divider()
        st.chat_message("assistant").write((element.get_attribute("innerHTML")))
