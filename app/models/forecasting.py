import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor

def run_arima(df):

    series = df["Price"]
    split = int(len(series) * 0.8)

    train = series[:split]
    test = series[split:]

    model = ARIMA(train, order=(5,1,0))
    model_fit = model.fit()

    pred = model_fit.forecast(steps=len(test))

    return test.values, pred.values


def run_rf(df):

    df["lag1"] = df["Price"].shift(1)
    df["lag2"] = df["Price"].shift(2)
    df = df.dropna()

    X = df[["lag1", "lag2"]]
    y = df["Price"]

    split = int(len(df) * 0.8)

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    return y_test.values, pred