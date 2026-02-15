from __future__ import annotations

import pandas as pd


def load_data(csv_path: str, date_col: str = "Date") -> pd.DataFrame:
    """
    Load dataset from a CSV and perform minimal, safe standardization.

    - Parses the date column (default: 'Date')
    - Sorts by time to support time-series workflow
    - Resets index
    """
    df = pd.read_csv(csv_path)

    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values(date_col).reset_index(drop=True)

    return df
