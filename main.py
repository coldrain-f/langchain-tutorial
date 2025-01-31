import streamlit as st


pages = {
    "Tutorial": [
        st.Page("./pages/tutorial/01.py", title="Basic LLM"),
        st.Page("./pages/tutorial/02.py", title="Advenced LLM"),
    ],
}
st.navigation(pages).run()
