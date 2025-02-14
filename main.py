import streamlit as st

from dotenv import load_dotenv

load_dotenv()

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
    "LangGraph": [
        st.Page(
            "./pages/langgraph/basic_llm_langgraph_agent_chatbot.py",
            title="Agent LLM - Tavily",
        ),
    ],
    "LangChain": [
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
        st.Page("./pages/utils/pdf-token-calculator.py", title="모델 비용 모의 계산기"),
    ],
}
st.navigation(pages).run()
