import streamlit as st

from components.chat_panel import render_chat_history
from services.api_client import APIClient
from state.session_state import initialize_state
from components.sidebar import render_sidebar

from components.sql_viewer import render_sql
from components.result_table import render_results
from components.metrics_panel import render_metrics
from components.download_panel import render_download_button
from components.feedback_panel import render_feedback

st.set_page_config(
    page_title="RAG SQL Chatbot",
    layout="wide",
)

initialize_state()
render_sidebar()

# Initialize last query result state
if "last_query" not in st.session_state:
    st.session_state.last_query = None

# Split layout for side-by-side chat and data visualization
col1, col2 = st.columns([1, 1.2])

with col1:
    st.title("🤖 RAG SQL Chatbot")
    render_chat_history()

with col2:
    if st.session_state.last_query:
        from components.kpi_panel import render_kpis
        render_kpis(
            st.session_state.last_query["results"],
            st.session_state.last_query["execution_time"],
            st.session_state.last_query["sql"]
        )
        render_sql(st.session_state.last_query["sql"])
        df = render_results(st.session_state.last_query["results"])
        render_download_button(st.session_state.last_query["results"])
        render_feedback()
        
        if df is not None:
            from components.charts.chart_generator import (
                ChartGenerator,
            )
            from components.charts.insight_generator import (
                InsightGenerator,
            )
            ChartGenerator.render(df)
            insights = InsightGenerator().generate(
                st.session_state.last_query.get("question", "Summarize results"),
                st.session_state.last_query["results"]
            )
            st.info(insights)

question = st.chat_input(
    "Ask a question about your data..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.spinner("Generating response..."):

        try:

            client = APIClient(
                "http://localhost:8089"
            )

            response = client.chat(
                question,
                st.session_state.conversation_id,
            )

            st.session_state.conversation_id = response.get("conversation_id")

            render_sql(
                response["sql"]
            )

            df = render_results(
                response["results"]
            )

            render_download_button(
                response["results"]
            )

            render_feedback()

            from components.charts.chart_generator import (
                ChartGenerator,
            )
            from components.charts.insight_generator import (
                InsightGenerator,
            )
            from components.kpi_panel import render_kpis

            # Render transient KPIs during execution
            render_kpis(
                response["results"],
                response["execution_time"],
                response["sql"]
            )

            if df is not None:
                ChartGenerator.render(
                    df
                )
                insights = InsightGenerator().generate(
                    question,
                    response["results"]
                )
                st.info(insights)

            st.session_state.last_query = {
                "question": question,
                "sql": response["sql"],
                "results": response["results"],
                "execution_time": response["execution_time"],
            }

            explanation = response.get(
                "explanation",
                "No explanation returned.",
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": explanation,
                }
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )