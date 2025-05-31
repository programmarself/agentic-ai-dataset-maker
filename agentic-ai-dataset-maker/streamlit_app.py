import streamlit as st
import pandas as pd
import openai
from utils.github_utils import push_to_github

openai.api_key = st.secrets.get("OPENAI_API_KEY", "your-openai-key-here")

DEFAULT_COLUMNS = 4
DEFAULT_ROWS = 10

def generate_column_names(topic, n_cols):
    prompt = f"Generate {n_cols} relevant column names for a dataset about '{topic}'"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return [col.strip(" -") for col in response['choices'][0]['message']['content'].strip().split('\n')]

def generate_data(topic, columns, n_rows):
    df = pd.DataFrame(columns=columns)
    for _ in range(n_rows):
        prompt = f"Provide a realistic row of data for topic '{topic}' with columns: {columns}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        row = response['choices'][0]['message']['content'].strip().split(',')
        df.loc[len(df)] = [r.strip() for r in row]
    return df

st.markdown("<h1 style='text-align: center;'>🤖 Agentic AI Dataset Maker</h1>", unsafe_allow_html=True)

topic = st.text_input("Enter a topic (e.g., Sports)", value="Sports")
n_cols = st.number_input("Number of columns", 1, 10, value=DEFAULT_COLUMNS)
n_rows = st.number_input("Number of rows", 1, 100, value=DEFAULT_ROWS)

use_custom_columns = st.checkbox("Use custom column names?")
columns = []

if use_custom_columns:
    custom_columns = st.text_area("Enter comma-separated column names:")
    if custom_columns:
        columns = [col.strip() for col in custom_columns.split(',')]
else:
    if topic and n_cols:
        columns = generate_column_names(topic, n_cols)

if st.button("Generate Dataset"):
    if columns:
        df = generate_data(topic, columns, n_rows)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, f"{topic}_dataset.csv", "text/csv")

        with st.expander("Push to GitHub"):
            github_token = st.text_input("GitHub Token", type="password")
            repo_name = st.text_input("Repo Name (e.g. username/repo)")
            if github_token and repo_name:
                result = push_to_github(repo_name, f"{topic}_dataset.csv", csv.decode('utf-8'), github_token)
                st.success(result)