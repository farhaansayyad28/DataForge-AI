def profile_dataset(data):
    total_cells = data.shape[0] * data.shape[1]
    total_missing = data.isnull().sum().sum()
    completeness_score = ((total_cells - total_missing) / total_cells) * 100
    duplicate_rows = int(data.duplicated().sum())
    unique_rows = data.shape[0] - duplicate_rows
    uniqueness_score = (unique_rows / data.shape[0]) * 100
    quality_score = (completeness_score + uniqueness_score) / 2
    
    profile = {
    "rows": data.shape[0],
    "columns": data.shape[1],
    "column_names": list(data.columns),
    "data_types": data.dtypes.astype(str).to_dict(),
    "missing_values": data.isnull().sum().to_dict(),
    "duplicate_rows": duplicate_rows,
    "completeness_score": completeness_score,
    "uniqueness_score": uniqueness_score,
    "quality_score": quality_score,
    "statistics": data.describe().to_dict()
}

    return profile