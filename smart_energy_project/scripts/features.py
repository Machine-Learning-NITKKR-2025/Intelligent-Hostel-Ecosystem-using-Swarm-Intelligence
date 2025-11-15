"""
Feature engineering script (fixed)
- Reads cleaned data from data/cleaned.csv
- Constructs a timestamp assuming rows are ordered at 3-hour intervals.
- Configurable START_DATE (change if you know the real first timestamp).
- Extracts datetime features (hour, day, month, weekday, is_weekend)
- Creates lag features for energy (t-1, t-2, t-3, t-4, t-8) and rolling means
- Saves features to data/features.csv
"""
import pandas as pd
import numpy as np
from pathlib import Path

# CONFIG: set this to the actual first timestamp of your data if you know it.
# Format: "YYYY-MM-DD HH:MM:SS"
# If you do NOT know the real start time, leave as default — relative timing will be preserved.
START_DATE = "2020-01-01 00:00:00"

CLEANED = Path(__file__).resolve().parents[1] / "data" / "cleaned.csv"
OUT = Path(__file__).resolve().parents[1] / "data" / "features.csv"

def add_datetime_features(df, ts_col):
    df['hour'] = df[ts_col].dt.hour
    df['day'] = df[ts_col].dt.day
    df['weekday'] = df[ts_col].dt.weekday
    df['is_weekend'] = df['weekday'] >= 5
    df['month_dt'] = df[ts_col].dt.month
    return df

def add_lag_features(df, target='energy_consumption_kwh', lags=[1,2,3,4,8]):
    # create lag features
    for lag in lags:
        df[f'lag_{lag}'] = df[target].shift(lag)
    # rolling windows: 3 and 8 samples (dataset is 3-hourly)
    df['roll_mean_3'] = df[target].shift(1).rolling(window=3, min_periods=1).mean()
    df['roll_mean_8'] = df[target].shift(1).rolling(window=8, min_periods=1).mean()
    return df

def main():
    df = pd.read_csv(CLEANED)
    n = len(df)
    if n == 0:
        raise RuntimeError("cleaned.csv is empty. Run data_prep.py first.")
    # create timestamp series at 3-hour intervals
    rng = pd.date_range(start=START_DATE, periods=n, freq='3H')
    df = df.copy()
    df['timestamp'] = rng
    # Ensure numeric month (keep original 'month' column if present)
    # Extract datetime features from the constructed timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = add_datetime_features(df, 'timestamp')
    # If 'month' column existed originally, keep both for comparison:
    # df['month_orig'] = df.get('month', np.nan)
    # Ensure target exists
    if 'energy_consumption_kwh' not in df.columns:
        raise RuntimeError("Target column 'energy_consumption_kwh' not found in cleaned.csv")
    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    # Add lag/rolling features
    df = add_lag_features(df, target='energy_consumption_kwh', lags=[1,2,3,4,8])
    # Drop rows with NaNs introduced by lags
    df = df.dropna().reset_index(drop=True)
    # Save
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Saved features to: {OUT} (shape: {df.shape})")

if __name__ == '__main__':
    main()
