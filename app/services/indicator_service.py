import pandas as pd
import numpy as np


def parse_volume(vol_str):
    vol_str = str(vol_str).strip().upper().replace(",", "")
    if vol_str in ("", "N/A", "NAN", "-"):
        return np.nan

    multipliers = {"K": 1e3, "M": 1e6, "B": 1e9}

    for suffix, mult in multipliers.items():
        if vol_str.endswith(suffix):
            return float(vol_str[:-1]) * mult

    return float(vol_str)


def process_indicators(file_path):

    df = pd.read_csv(file_path)
    df.columns = [c.strip().strip('"') for c in df.columns]

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date")

    # clean price
    df["Price"] = pd.to_numeric(
        df["Price"].astype(str).str.replace(",", ""),
        errors="coerce"
    )

    # ───────────── Indicators ─────────────
    df["SMA5"] = df["Price"].rolling(5).mean()
    df["SMA10"] = df["Price"].rolling(10).mean()
    df["SMA20"] = df["Price"].rolling(20).mean()

    df["EMA5"] = df["Price"].ewm(span=5, adjust=False).mean()
    df["EMA10"] = df["Price"].ewm(span=10, adjust=False).mean()
    df["EMA20"] = df["Price"].ewm(span=20, adjust=False).mean()

    # signals
    df["Signal"] = np.where(df["EMA5"] > df["EMA10"], 1, 0)
    df["Crossover"] = df["Signal"].diff()

    df = df.dropna()

    return df