import streamlit as st

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

pages = {
    "Tutorial": [
        st.Page("./pages/tutorial/basic_llm.py", title="Basic LLM"),
        st.Page(
            "./pages/tutorial/basic_llm_use_chain.py", title="Basic LLM - Use Chain"
        ),
        st.Page(
            "./pages/tutorial/basic_llm_multi_turn.py", title="Basic LLM - Multi-Turn"
        ),
        st.Page("./pages/tutorial/rag_llm_pdf_loader.py", title="RAG LLM - PDF Loader"),
    ],
    "유틸리티": [
        st.Page("./pages/utils/langchain.py", title="LangChain"),
        st.Page("./pages/utils/pdf-token-calculator.py", title="모델 비용 모의 계산기"),
        st.Page("./pages/utils/web_base_loader.py", title="JPDB Web Crawling"),
        st.Page("./pages/utils/web_base_loader2.py", title="Naver Dict Web Crawling"),
    ],
}
st.navigation(pages).run()
