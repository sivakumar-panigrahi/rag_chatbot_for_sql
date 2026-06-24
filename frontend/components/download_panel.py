import pandas as pd
import streamlit as st


def render_download_button(
    results: list[dict],
):

    if not results:
        return

    df = pd.DataFrame(results)

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="query_results.csv",
        mime="text/csv",
    )