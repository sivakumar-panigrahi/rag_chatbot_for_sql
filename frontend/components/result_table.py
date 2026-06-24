# Result table UI component
import pandas as pd
import streamlit as st


def render_results(
    results: list[dict],
):

    st.subheader(
        "Query Results"
    )

    if not results:

        st.info(
            "No rows returned."
        )

        return None

    df = pd.DataFrame(
        results
    )

    st.dataframe(
        df,
        use_container_width=True,
    )

    return df