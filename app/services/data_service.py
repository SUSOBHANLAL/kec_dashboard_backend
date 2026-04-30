import pandas as pd

def process_data(df: pd.DataFrame):

    df.columns = [c.strip().strip('"') for c in df.columns]

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values("Date")

    df["Price"] = df["Price"].astype(str).str.replace(",", "").astype(float)

    return df