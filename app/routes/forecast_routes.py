# from flask import Blueprint, request, jsonify
# import pandas as pd

# from app.services.data_service import process_data
# from app.models.forecasting import run_arima, run_rf
# from app.utils.metrics import evaluate

# forecast_bp = Blueprint("forecast", __name__)

# @forecast_bp.route("/forecast", methods=["POST"])
# def forecast():

#     if 'file' not in request.files:
#         return jsonify({"error": "CSV file required"}), 400

#     file = request.files['file']
#     model = request.args.get("model", "arima")

#     try:
#         df = pd.read_csv(file)
#         df = process_data(df)

#         if model == "arima":
#             y_test, pred = run_arima(df)
#         elif model == "rf":
#             y_test, pred = run_rf(df)
#         else:
#             return jsonify({"error": "Invalid model"}), 400

#         metrics = evaluate(y_test, pred)

#         return jsonify({
#             "model": model,
#             "metrics": metrics,
#             "predictions": pred[:20].tolist()
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500










from flask import Blueprint, request, jsonify
import pandas as pd

from app.config import CSV_FILES
from app.services.data_service import process_data
from app.models.forecasting import run_arima, run_rf
from app.utils.metrics import evaluate

forecast_bp = Blueprint("forecast", __name__)

@forecast_bp.route("/forecast", methods=["GET"])
def forecast():

    ticker = request.args.get("ticker")
    model = request.args.get("model", "arima")

    if not ticker:
        return jsonify({"error": "Ticker is required"}), 400

    ticker = ticker.upper()

    if ticker not in CSV_FILES:
        return jsonify({"error": f"Ticker '{ticker}' not found"}), 404

    try:
        # Load CSV from path
        file_path = CSV_FILES[ticker]
        df = pd.read_csv(file_path)

        df = process_data(df)

        if model == "arima":
            y_test, pred = run_arima(df)
        elif model == "rf":
            y_test, pred = run_rf(df)
        else:
            return jsonify({"error": "Invalid model"}), 400

        metrics = evaluate(y_test, pred)

        return jsonify({
            "ticker": ticker,
            "model": model,
            "metrics": metrics,
            "predictions": pred[:20].tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500