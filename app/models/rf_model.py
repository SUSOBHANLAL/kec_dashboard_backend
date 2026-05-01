from sklearn.ensemble import RandomForestRegressor
import numpy as np

def run_rf(series):
    df = series.to_frame("Price")

    df["lag_1"] = df["Price"].shift(1)
    df["lag_2"] = df["Price"].shift(2)
    df["lag_3"] = df["Price"].shift(3)

    df = df.dropna()

    X = df[["lag_1", "lag_2", "lag_3"]]
    y = df["Price"]

    split = int(len(df) * 0.8)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X[:split], y[:split])

    preds = model.predict(X[split:])

    return preds.tolist()