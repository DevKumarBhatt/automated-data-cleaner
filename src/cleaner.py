
import pandas as pd


def analyze_data(df):
    """Generate a summary of data quality before cleaning."""
    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": int(df.isna().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
    }


def clean_data(df, fill_missing=True, remove_duplicates=True):
    """Clean column names, missing values, and duplicate rows."""
    cleaned_df = df.copy()

    # Standardize column names
    cleaned_df.columns = (
        cleaned_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Remove duplicate rows if selected
    if remove_duplicates:
        cleaned_df = cleaned_df.drop_duplicates()

    # Fill missing values if selected
    if fill_missing:
        for column in cleaned_df.columns:
            if cleaned_df[column].isna().any():
                if pd.api.types.is_numeric_dtype(cleaned_df[column]):
                    median_value = cleaned_df[column].median()
                    cleaned_df[column] = cleaned_df[column].fillna(median_value)
                else:
                    cleaned_df[column] = cleaned_df[column].fillna("Unknown")

    return cleaned_df
