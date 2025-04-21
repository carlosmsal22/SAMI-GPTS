
import pandas as pd

def summarize_dataframe(df):
    summary = {}
    for col in df.select_dtypes(include='number').columns:
        summary[col] = {
            "mean": df[col].mean(),
            "std": df[col].std(),
            "min": df[col].min(),
            "max": df[col].max(),
        }
    return pd.DataFrame(summary).T
