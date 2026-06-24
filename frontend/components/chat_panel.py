# Chat panel UI component
import streamlit as st


def render_chat_history():

    for message in (
        st.session_state.messages
    ):

        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )