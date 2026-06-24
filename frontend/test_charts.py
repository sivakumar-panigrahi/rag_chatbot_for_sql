import pandas as pd
from components.charts.chart_generator import ChartGenerator
from components.charts.insight_generator import InsightGenerator

# Sample products data resembling actual database results
results = [
    {"id": 1, "name": "Allison Hill", "price": 99.9, "stock": 100},
    {"id": 2, "name": "Jonathan Johnson", "price": 49.9, "stock": 50},
]

df = pd.DataFrame(results)
print("DataFrame columns:", df.columns)
print("Numeric columns:", df.select_dtypes(include="number").columns)

# Mock streamlit to print chart info instead of rendering it
import streamlit as st
def mock_bar_chart(data, x, y):
    print(f"Mock st.bar_chart: x={x}, y={y}")

st.bar_chart = mock_bar_chart

ChartGenerator.render(df)
insight = InsightGenerator.generate(df)
print("Generated Insight:", insight)
