from statsmodels.tsa.arima.model import ARIMA

def run_arima(series):
    train_size = int(len(series) * 0.8)

    train = series[:train_size]
    test = series[train_size:]

    model = ARIMA(train, order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=len(test))

    return forecast.tolist()