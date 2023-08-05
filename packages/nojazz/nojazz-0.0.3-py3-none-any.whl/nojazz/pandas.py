import pandas as pd
import numpy as np


def fill_between_valid(series: pd.Series, value=0) -> pd.Series:
    """
    Finds the first and last valid (non-null) values in
    a Series and fills all NULL values with `value`
    """
    series = series.copy()

    first_valid = series.first_valid_index()
    last_valid = series.last_valid_index()

    series.loc[first_valid : last_valid + 1] = series[
        first_valid : last_valid + 1
    ].fillna(value)
    return series


def fill_time_series_nulls(df: pd.DataFrame, value=0) -> pd.DataFrame:
    """
    Given a DataFrame, `df`, with:
        - rows of agents
        - columns of observations
        - cells of observed values

    goes through and applies `fill_between_valid`, row-wise,
    filling the appropriate cells with `value` and returning
    the new DataFrame
    """
    df = df.copy()

    for idx, row in df.iterrows():
        df.loc[idx] = fill_between_valid(row, value)

    return df


def realign_nonnull_data(series: pd.Series) -> pd.Series:
    """
    Makes the first non-null value the first index and
    moves all other values, accordingly, appending NULL
    values to the end, to preserve the same `len(series)`
    """

    series = series.copy()
    result = series.copy()

    length = len(series)

    first_idx = series.first_valid_index()

    if first_idx:
        num_valid_values = length - first_idx
        num_to_null_pad = length - num_valid_values

        result.loc[: num_valid_values - 1] = series.loc[first_idx:].values
        result.loc[num_valid_values:] = np.nan

    return result


def realign_time_series_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Used to translate observations (e.g. dates) to ordinal data
    (e.g. first, second, third, ... data points for each row)

    For each row in a DataFrame, finds the first non-null column and
    shifts the entire row such that the first column is each row's
    first_valid_index data-- padding the end with NULL values to
    preserve `df.shape`
    """
    df = df.copy()

    for idx, row in df.iterrows():
        df.loc[idx] = realign_nonnull_data(row)

    return df
