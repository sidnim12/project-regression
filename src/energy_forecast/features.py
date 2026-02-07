import pandas as pd


def add_lag_features(
    df: pd.DataFrame,
    target_col: str = "Production",
    time_col: str = "Date",
    lags=(1, 24),
):
    df = df.sort_values(time_col).copy()

    for lag in lags:
        df[f"{target_col}_lag_{lag}"] = df[target_col].shift(lag)

    return df


def add_rolling_features(
    df: pd.DataFrame,
    target_col: str = "Production",
    time_col: str = "Date",
    windows=(24,),
):
    df = df.sort_values(time_col).copy()

    for w in windows:
        df[f"{target_col}_rollmean_{w}"] = (
            df[target_col]
            .shift(1)
            .rolling(window=w, min_periods=w)
            .mean()
        )

    return df
