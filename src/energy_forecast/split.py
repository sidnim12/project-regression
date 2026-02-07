from __future__ import annotations

import pandas as pd


def time_split(
    df: pd.DataFrame,
    time_col: str = "Date",
    train_end=None,
    val_end=None,
):
    """
    Leakage-safe chronological split.

    train: time <= train_end
    val:   train_end < time <= val_end
    test:  time > val_end

    train_end and val_end can be:
    - pandas.Timestamp
    - datetime
    - or date strings like "2022-12-31" (if time_col is datetime)
    """
    if time_col not in df.columns:
        raise KeyError(f"'{time_col}' not found in columns: {list(df.columns)}")

    df = df.sort_values(time_col).reset_index(drop=True)

    if train_end is None or val_end is None:
        # Default: 70/15/15 by row count (still time-ordered)
        n = len(df)
        train_end_idx = int(n * 0.70)
        val_end_idx = int(n * 0.85)

        train = df.iloc[:train_end_idx].copy()
        val = df.iloc[train_end_idx:val_end_idx].copy()
        test = df.iloc[val_end_idx:].copy()
        return train, val, test

    train_end = pd.to_datetime(train_end)
    val_end = pd.to_datetime(val_end)

    train = df[df[time_col] <= train_end].copy()
    val = df[(df[time_col] > train_end) & (df[time_col] <= val_end)].copy()
    test = df[df[time_col] > val_end].copy()

    return train, val, test
