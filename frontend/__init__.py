import streamlit as st

from components.chat_panel import (
    render_chat_history,
)
from services.api_client import (
    APIClient,
)
from state.session_state import (
    initialize_state,
)

st.set_page_config(
    page_title="RAG SQL Chatbot",
    layout="wide",
)

initialize_state()

client = APIClient(
    "http://localhost:8089"
)

st.title(
    "RAG SQL Chatbot"
)

render_chat_history()

question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    response = client.chat(
        question
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response[
                "explanation"
            ],
        }
    )

    st.rerun()