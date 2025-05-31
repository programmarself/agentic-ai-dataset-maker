import streamlit as st
import pandas as pd
import random
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else None)

def generate_column_names(topic, n_cols):
    prompt = f"Generate {n_cols} relevant column names for a dataset about '{topic}'."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    columns_text = response.choices[0].message.content.strip()
    columns = [col.strip() for col in columns_text.split(",")]
    return columns[:n_cols]

def generate_dummy_data(columns, n_rows):
    data = []
    for _ in range(n_rows):
        row = [f"{col}_{random.randint(1, 100)}" for col in columns]
        data.append(row)
    return pd.DataFrame(data, columns=columns)

st.title("📊 Agentic AI Dataset Maker")

topic = st.text_input("Enter a topic (e.g., 'Sports', 'Healthcare')")
n_cols = st.number_input("Number of columns (default 5)", min_value=1, max_value=20, value=5)
n_rows = st.number_input("Number of rows (default 10)", min_value=1, max_value=1000, value=10)
custom_columns = st.text_input("Optional: Enter custom column names (comma separated)")

columns = []
if custom_columns:
    columns = [col.strip() for col in custom_columns.split(',')]
elif topic and n_cols:
    columns = generate_column_names(topic, n_cols)

if st.button("Generate Dataset"):
    if columns:
        df = generate_dummy_data(columns, n_rows)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, f"{topic}_dataset.csv", "text/csv")
    else:
        st.warning("Please provide a topic or custom column names.")