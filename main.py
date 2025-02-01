import streamlit as st


pages = {
    "Tutorial": [
        st.Page("./pages/tutorial/basic_llm.py", title="Basic LLM"),
        st.Page(
            "./pages/tutorial/basic_llm_use_chain.py", title="Basic LLM - Use Chain"
        ),
        st.Page("./pages/tutorial/rag_llm_pdf_loader.py", title="RAG LLM - PDF Loader"),
    ],
    "Utils": [
        st.Page("./pages/utils/langchain.py", title="LangChain"),
    ],
}
st.navigation(pages).run()
