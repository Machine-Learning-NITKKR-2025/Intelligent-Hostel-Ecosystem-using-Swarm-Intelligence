"""Data preparation script
- Loads the CSV
- Basic cleaning: parse datetime if possible, impute missing values (median for numeric, mode for categorical)
- Saves cleaned CSV to data/cleaned.csv
"""
import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = 'data/hostel_energy_data_3hourly.csv'
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "cleaned.csv"

def infer_datetime(df):
    # find a column that looks like datetime
    for col in df.columns:
        try:
            parsed = pd.to_datetime(df[col], errors='coerce')
            if parsed.notna().mean() > 0.7 and parsed.nunique() > 10:
                df[col] = parsed
                return col, df
        except Exception:
            pass
    return None, df

def main():
    print("Loading raw data...")
    df = pd.read_csv(RAW_PATH)
    print(f"Raw shape: {df.shape}")

    dt_col, df = infer_datetime(df)
    if dt_col:
        print(f"Detected datetime column: {dt_col}")
    else:
        print("No clear datetime column detected. You may need to specify it manually.")

    # Drop rows with missing target if detected (energy_consumption_kwh)
    if 'energy_consumption_kwh' in df.columns:
        df = df.dropna(subset=['energy_consumption_kwh'])

    # Impute numerics with median, categoricals with mode
    for col in df.columns:
        if col == dt_col:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            med = df[col].median()
            df[col] = df[col].fillna(med)
        else:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode().iloc[0])

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved cleaned data to: {OUT_PATH} (shape: {df.shape})")

if __name__ == '__main__':
    main()
