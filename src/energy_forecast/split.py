from __future__ import annotations
from dataclasses import dataclass
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


@dataclass(frozen=True)
class WalkForwardFold:
    fold: int
    train: pd.DataFrame
    val: pd.DataFrame


def walk_forward_splits(
    df: pd.DataFrame,
    time_col: str = "Date",
    initial_train_frac: float = 0.50,
    val_frac: float = 0.10,
    n_folds: int = 4,
) -> list[WalkForwardFold]:
    """
    Expanding-window walk-forward splits (leakage-safe).

    Example (default):
      Fold 1: train 0–50%, val 50–60%
      Fold 2: train 0–60%, val 60–70%
      Fold 3: train 0–70%, val 70–80%
      Fold 4: train 0–80%, val 80–90%

    Notes:
    - Data is sorted by time_col.
    - Folds are created by row index (time-ordered).
    - The tail portion after the last validation window is left unused here
      (commonly reserved as a final holdout test set).
    """
    if time_col not in df.columns:
        raise KeyError(f"'{time_col}' not found in columns: {list(df.columns)}")

    if not (0 < initial_train_frac < 1):
        raise ValueError("initial_train_frac must be between 0 and 1.")
    if not (0 < val_frac < 1):
        raise ValueError("val_frac must be between 0 and 1.")
    if n_folds < 1:
        raise ValueError("n_folds must be >= 1.")

    df_sorted = df.sort_values(time_col).reset_index(drop=True)
    n = len(df_sorted)

    init_train_end = int(n * initial_train_frac)
    val_size = int(n * val_frac)

    if init_train_end <= 0:
        raise ValueError("Initial train window is empty. Increase initial_train_frac.")
    if val_size <= 0:
        raise ValueError("Validation window is empty. Increase val_frac or dataset size.")

    folds: list[WalkForwardFold] = []
    train_end = init_train_end

    for i in range(1, n_folds + 1):
        val_start = train_end
        val_end = train_end + val_size

        if val_end > n:
            # Not enough data for this fold
            break

        train_df = df_sorted.iloc[:train_end].copy()
        val_df = df_sorted.iloc[val_start:val_end].copy()

        if len(val_df) == 0 or len(train_df) == 0:
            break

        folds.append(WalkForwardFold(fold=i, train=train_df, val=val_df))

        # expanding window: extend train to include the validation window
        train_end = val_end

    if len(folds) == 0:
        raise ValueError(
            "No folds were created. Try reducing n_folds or val_frac, "
            "or increasing dataset size."
        )

    return folds