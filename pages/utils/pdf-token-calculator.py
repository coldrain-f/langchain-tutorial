import streamlit as st
import pandas as pd
import os

from typing import List

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents.base import Document

if not os.path.exists(".cache"):
    os.mkdir(".cache")

if not os.path.exists(".cache/buffer"):
    os.mkdir(".cache/buffer")


def calculate_text_size_and_cost(
    documents: List[Document], usd_cost: str, token_unit: str
):
    # 모든 문서 내용을 하나의 텍스트로 결합
    combined_text = "".join(doc.page_content for doc in documents)

    # 비용 계산 상수
    TOKENS_PER_KILO = 1000  # 1K
    TOKENS_PER_MILLION = 1000000  # 1M
    KRW_EXCHANGE_RATE = 1459

    # 토큰 수와 비용 계산
    token_count = len(combined_text)
    size = token_count // TOKENS_PER_KILO  # 사이즈는 K단위

    # Kilo 계산: 263K * 0.02
    # Million 계산: (263K * 0.02) / 1000
    usd_display_cost = size * float(usd_cost)
    if token_unit == "Million":
        usd_display_cost = (size * float(usd_cost)) / 1000

    krw_display_cost = usd_display_cost * KRW_EXCHANGE_RATE

    # 데이터프레임 생성
    cost_data = {
        "사이즈": [f"{size}K"],
        "페이지": [f"{len(documents)}"],
        "USD(소수점 2자리)": [f"${usd_display_cost:.2f}"],
        "KRW(소수점 버림)": [f"₩{krw_display_cost:.0f}"],
    }

    return pd.DataFrame(cost_data)


st.title("모델 비용 모의 계산기")
st.write(
    """토큰 계산 방식은 AI 기업, 모델, 언어마다 다릅니다. 대체로 한글은 글자 단위로, 영어는 단어 단위로 토큰이 계산되는 경향이 있습니다.
이 계산기는 간단한 비용 추정을 위해 모든 문자를 1토큰으로 계산합니다. 실제 토큰 수와는 차이가 있으니 참고용으로만 사용해 주세요."""
)

st.header("임베딩(Embedding)")
st.caption("계산 환율: $1 → ₩1459.29")

selected_token_unit = st.selectbox(
    "계산 기준 단위를 선택해 주세요.", ("Kilo", "Million")
)

unit_display_text = ""
if selected_token_unit == "Kilo":
    unit_display_text = "1,000(1K)"
elif selected_token_unit == "Million":
    unit_display_text = "1,000,000(1M)"

usd_cost = st.text_input(
    f"{unit_display_text} 토큰당 계산될 미국 달러(USD)를 입력해 주세요.",
    value="0",
    help=f"모델의 가격이 {unit_display_text} 토큰당 $0.00002인 경우, 0.00002를 입력하세요.",
)

uploaded_file = st.file_uploader(
    "비용 계산을 위한 문서 파일을 업로드해 주세요.", type=["pdf"]
)

if uploaded_file:
    # 임시 저장 공간에 업로드 파일 저장
    file_content = uploaded_file.read()
    file_path = f"./.cache/buffer/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    calculate_button = st.button("계산하기")

    if calculate_button:
        with st.spinner("잠시만 기다려주세요...", show_time=True):
            loader = PyMuPDFLoader(file_path)
            documents = loader.load()

            cost_df = calculate_text_size_and_cost(
                documents, usd_cost, selected_token_unit
            )
            st.subheader("모의 계산 결과")
            st.dataframe(cost_df, use_container_width=True, hide_index=True)

            for document in documents:
                with st.expander(f"{document.metadata['page'] + 1} 페이지"):
                    st.write(document.page_content)

            # 임시 저장공간에 저장 된 파일을 삭제
            try:
                os.remove(file_path)
            except FileNotFoundError:
                st.error("파일을 찾을 수 없습니다.")
            except PermissionError:
                st.error("파일을 삭제할 권한이 없습니다.")
            except Exception as e:
                st.error(f"파일 삭제 중 오류가 발생했습니다: {e}")
