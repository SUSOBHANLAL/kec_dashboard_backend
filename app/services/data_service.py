import pandas as pd

# def process_data(df: pd.DataFrame):

#     df.columns = [c.strip().strip('"') for c in df.columns]

#     df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
#     df = df.sort_values("Date")

#     df["Price"] = df["Price"].astype(str).str.replace(",", "").astype(float)

#     return df




def process_data(df):

    df.columns = [c.strip().strip('"') for c in df.columns]

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values("Date")

    df["Price"] = df["Price"].astype(str).str.replace(",", "").astype(float)

    # 🔥 REQUIRED FOR YOUR NEW API
    df["MA10"] = df["Price"].rolling(10).mean()
    df["MA20"] = df["Price"].rolling(20).mean()

    df["Returns"] = df["Price"].pct_change()
    df["Volatility"] = df["Returns"].rolling(10).std()

    return df