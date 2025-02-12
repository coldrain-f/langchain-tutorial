import streamlit as st

# 전체 폰트 설정
st.markdown(
    """
            <style>
            @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");
            * {
                font-family: 'Pretendard' !important
            }
            </style>
            """,
    unsafe_allow_html=True,
)

# 사이드바 메뉴 설정
pages = {
    "Tutorial": [
        st.Page("./pages/tutorial/basic_llm.py", title="Basic LLM"),
        st.Page(
            "./pages/tutorial/basic_llm_use_chain.py", title="Basic LLM - Use Chain"
        ),
        st.Page(
            "./pages/tutorial/basic_llm_multi_turn.py", title="Basic LLM - Multi-Turn"
        ),
    ],
    "LangGraph": [
        st.Page(
            "./pages/langgraph/basic_llm_langgraph.py", title="LangGraph 기본 구조 확인"
        ),
    ],
    "RAG": [
        st.Page("./pages/tutorial/rag_llm_pdf_loader.py", title="RAG LLM - PDF Loader"),
    ],
    "프롬프트": [
        st.Page(
            "./pages/prompt/few_shot_prompt_template.py",
            title="Few Shot 적용하기",
        ),
    ],
    "유틸리티": [
        st.Page("./pages/utils/langchain.py", title="LangChain"),
        st.Page("./pages/utils/pdf-token-calculator.py", title="모델 비용 모의 계산기"),
    ],
    "크롤링": [
        st.Page("./pages/utils/web_base_loader.py", title="JPDB 웹 크롤링"),
        st.Page(
            "./pages/utils/web_base_loader2.py", title="네이버 일본어 사전 웹 크롤링"
        ),
    ],
}
st.navigation(pages).run()
