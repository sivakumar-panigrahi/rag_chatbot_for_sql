# Metrics panel UI component
import streamlit as st


def render_metrics(
    execution_time: float,
    row_count: int,
):

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Execution Time",
            f"{execution_time:.3f}s",
        )

    with col2:

        st.metric(
            "Rows Returned",
            row_count,
        )