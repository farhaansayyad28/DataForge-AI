import streamlit as st
from src.ingestion.loader import load_dataset


st.set_page_config(
    page_title="DataForge AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataForge AI")
st.write("A simple data engineering platform for preparing and understanding datasets.")

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx", "json"]
)

if uploaded_file is not None:
    try:
        data = load_dataset(uploaded_file)

        st.success("Dataset loaded successfully!")

        st.subheader("Dataset Preview")
        st.dataframe(data.head(10))

        st.write("Rows:", data.shape[0])
        st.write("Columns:", data.shape[1])

    except Exception as error:
        st.error(f"Could not load the dataset: {error}")