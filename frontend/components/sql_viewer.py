# SQL viewer UI component
import streamlit as st


def render_sql(sql: str):

    st.subheader("Generated SQL")

    st.code(
        sql,
        language="sql",
    )