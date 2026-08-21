def profile_dataset(data):
    profile = {
        "rows": data.shape[0],
        "columns": data.shape[1],
        "column_names": list(data.columns),
        "data_types": data.dtypes.astype(str).to_dict(),
        "missing_values": data.isnull().sum().to_dict(),
        "duplicate_rows": int(data.duplicated().sum()),
        "statistics": data.describe().to_dict()
    }

    return profile