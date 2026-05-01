from app.services.load_data_service import load_data
from app.models.arima_model import run_arima
from app.models.rf_model import run_rf
from app.models.lstm_model import run_lstm

def run_all_models(file_path):
    df = load_data(file_path)
    series = df["Price"]

    return {
        "arima": run_arima(series),
        "random_forest": run_rf(series),
        "lstm": run_lstm(series)
    }