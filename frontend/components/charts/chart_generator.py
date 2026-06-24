import pandas as pd
import streamlit as st


class ChartGenerator:

    @staticmethod
    def render(df: pd.DataFrame):

        if df.empty:
            return

        if len(df.columns) < 2:
            return

        numeric_cols = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        if not numeric_cols:
            return

        value_col = numeric_cols[0]

        non_numeric_cols = [
            col
            for col in df.columns
            if col not in numeric_cols
        ]

        category_col = (
            non_numeric_cols[0]
            if non_numeric_cols
            else df.columns[0]
        )

        st.subheader(
            "Visualization"
        )

        # ---------- Time Series ----------
        if (
            "date" in category_col.lower()
            or "time" in category_col.lower()
        ):

            st.line_chart(
                df.set_index(
                    category_col
                )[value_col]
            )

            return

        # ---------- Percentage / Share ----------
        if any(
            keyword in value_col.lower()
            for keyword in [
                "percent",
                "percentage",
                "share",
            ]
        ):

            pie_df = df[
                [category_col, value_col]
            ]

            st.write(
                "Pie Chart"
            )

            st.pyplot(
                pie_df.set_index(
                    category_col
                ).plot.pie(
                    y=value_col,
                    legend=False,
                ).figure
            )

            return

        # ---------- Top N ----------
        if len(df) <= 15:

            st.bar_chart(
                data=df,
                x=category_col,
                y=value_col,
            )

            return

        # ---------- Large Dataset ----------
        st.line_chart(
            data=df,
            x=category_col,
            y=value_col,
        )