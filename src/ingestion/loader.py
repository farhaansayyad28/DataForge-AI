import pandas as pd


def load_dataset(file):
    file_name = file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(file)

    if file_name.endswith(".xlsx"):
        return pd.read_excel(file)

    if file_name.endswith(".json"):
        return pd.read_json(file)

    raise ValueError("Unsupported file format")