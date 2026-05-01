def load_data(file_path):
    import pandas as pd

    df = pd.read_csv(file_path)

    df.columns = [c.strip().strip('"') for c in df.columns]

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["Date"])
    df = df.sort_values("Date")

    df["Price"] = pd.to_numeric(
        df["Price"].astype(str).str.replace(",", ""),
        errors="coerce"
    )

    df = df.dropna().reset_index(drop=True)

    return df