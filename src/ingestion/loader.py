import pandas as pd


def load_dataset(file):
    file_name = file.name.lower()

    if file_name.endswith(".csv"):
        # Check for a zero-byte file, then rewind so pandas reads from the start.
        if not file.read(1):
            raise ValueError(
                "The CSV file is empty. Upload a CSV with a header row."
            )
        file.seek(0)
        return pd.read_csv(file)

    if file_name.endswith(".xlsx"):
        return pd.read_excel(file)

    if file_name.endswith(".json"):
        return pd.read_json(file)

    raise ValueError("Unsupported file format")
