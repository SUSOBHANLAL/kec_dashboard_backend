import pandas as pd
from sklearn.linear_model import LinearRegression

def run_predictive_model(file_path):
    df = pd.read_csv(file_path)

    # ✅ FIX 1: clean commas and convert to float
    df["Price"] = df["Price"].astype(str).str.replace(",", "")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    # remove invalid rows
    df = df.dropna()

    # ⚠️ FIX 2: reset index after dropna (important for shift alignment)
    df = df.reset_index(drop=True)

    X = df[["Price"]].shift(1).dropna()
    y = df["Price"][1:]

    # align X and y properly
    X = X.iloc[:, 0].values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict(X[-5:])

    return prediction.tolist()