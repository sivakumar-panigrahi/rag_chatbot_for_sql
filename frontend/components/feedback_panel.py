import streamlit as st


def render_feedback():

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "👍 Helpful"
        ):
            st.success(
                "Feedback recorded"
            )

    with col2:

        if st.button(
            "👎 Not Helpful"
        ):
            st.warning(
                "Feedback recorded"
            )