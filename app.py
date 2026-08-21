import streamlit as st
from src.ingestion.loader import load_dataset
from src.profiling.profiler import profile_dataset


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

        profile = profile_dataset(data)

        st.subheader("Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        total_missing = sum(profile["missing_values"].values())

        with col1:
            st.metric("Rows", profile["rows"])

        with col2:
            st.metric("Columns", profile["columns"])

        with col3:
            st.metric("Missing Values", total_missing)

        with col4:
            st.metric("Duplicate Rows", profile["duplicate_rows"])

        st.subheader("Column Information")

        column_info = {
            "Column": profile["column_names"],
            "Data Type": [
                profile["data_types"][column]
                for column in profile["column_names"]
            ],
            "Missing Values": [
                profile["missing_values"][column]
                for column in profile["column_names"]
            ]
        }

        st.dataframe(
            column_info,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Basic Statistics")

        st.dataframe(
            profile["statistics"],
            use_container_width=True
        )

    except Exception as error:
        st.error(f"Could not load the dataset: {error}")