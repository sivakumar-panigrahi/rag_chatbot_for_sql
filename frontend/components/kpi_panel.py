import streamlit as st
import sqlglot
from sqlglot import exp


def render_kpis(results: list, execution_time: float, sql: str):
    """
    Renders top-level KPIs: Rows, Time, and Tables using st.metric.
    """
    kpi1, kpi2, kpi3 = st.columns(3)

    # Extract table names using sqlglot
    try:
        parsed = sqlglot.parse_one(sql, dialect="postgres")
        tables = {t.name for t in parsed.find_all(exp.Table) if t.name}
        tables_str = ", ".join(tables) if tables else "N/A"
    except Exception:
        tables_str = "N/A"

    kpi1.metric(label="Rows", value=str(len(results)))
    kpi2.metric(
        label="Time",
        value=f"{execution_time:.2f} sec"
        if isinstance(execution_time, (int, float))
        else f"{execution_time} sec",
    )
    kpi3.metric(label="Tables", value=tables_str)
    st.divider()
