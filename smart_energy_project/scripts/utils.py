import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

def load_data(path):
    df = pd.read_csv(path)
    return df

def save_df(df, path):
    df.to_csv(path, index=False)

def time_train_test_split(df, time_col, test_size=0.2):
    df_sorted = df.sort_values(time_col).reset_index(drop=True)
    split_idx = int(len(df_sorted)*(1-test_size))
    train = df_sorted.iloc[:split_idx].copy()
    test = df_sorted.iloc[split_idx:].copy()
    return train, test
