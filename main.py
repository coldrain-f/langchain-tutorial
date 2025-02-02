import streamlit as st


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
    "Utils": [
        st.Page("./pages/utils/langchain.py", title="LangChain"),
        st.Page("./pages/utils/web_base_loader.py", title="JPDB Web Crawling"),
    ],
}
st.navigation(pages).run()
