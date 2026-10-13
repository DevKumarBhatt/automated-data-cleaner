
import streamlit as st
import pandas as pd
from src.cleaner import analyze_data, clean_data

st.set_page_config(
    page_title="Automated Data Cleaner",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Automated Data Cleaner")
st.write("Upload your CSV file, analyze data quality, clean your data, and download the result.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("📊 Original Data")
        col1, col2 = st.columns(2)

        original_stats = analyze_data(df)

        with col1:
            st.metric("Total Rows", original_stats["Rows"])
            st.metric("Total Columns", original_stats["Columns"])

        with col2:
            st.metric("Missing Values", original_stats["Missing Values"])
            st.metric("Duplicate Rows", original_stats["Duplicate Rows"])

        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("⚙️ Cleaning Options")

        fill_missing = st.checkbox("Fill missing values", value=True)
        remove_duplicates = st.checkbox("Remove duplicate rows", value=True)

        if st.button("✨ Clean My Data", type="primary"):
            cleaned_df = clean_data(
                df,
                fill_missing=fill_missing,
                remove_duplicates=remove_duplicates
            )

            st.subheader("✅ Cleaned Data")

            cleaned_stats = analyze_data(cleaned_df)

            col1, col2, col3 = st.columns(3)
            col1.metric("Rows After Cleaning", cleaned_stats["Rows"])
            col2.metric("Missing Values Left", cleaned_stats["Missing Values"])
            col3.metric("Duplicate Rows Left", cleaned_stats["Duplicate Rows"])

            st.dataframe(cleaned_df.head(10), use_container_width=True)

            csv_data = cleaned_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download Cleaned CSV",
                data=csv_data,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Unable to process this file: {e}")
else:
    st.info("👆 Upload a CSV file to get started.")
