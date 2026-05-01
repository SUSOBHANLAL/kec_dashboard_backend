

from flask import Blueprint, request, jsonify
import pandas as pd
from flask_cors import cross_origin

from app.config import CSV_FILES
from app.services.data_service import process_data
from app.models.forecasting import run_arima, run_rf
from app.utils.metrics import evaluate

forecast_bp = Blueprint("forecast", __name__)


@forecast_bp.route("/forecast", methods=["GET"])
@cross_origin()
def forecast():

    ticker = request.args.get("ticker")
    model = request.args.get("model", "arima")

    # ✅ Validation
    if not ticker:
        return jsonify({"error": "Ticker is required"}), 400

    ticker = ticker.upper()

    if ticker not in CSV_FILES:
        return jsonify({"error": f"Ticker '{ticker}' not found"}), 404

    try:
        # 📂 Load CSV
        file_path = CSV_FILES[ticker]
        df = pd.read_csv(file_path)

        # 🔧 Process data
        df = process_data(df)

        # 🔮 Run model
        if model == "arima":
            y_test, pred = run_arima(df)
        elif model == "rf":
            y_test, pred = run_rf(df)
        else:
            return jsonify({"error": "Invalid model"}), 400

        # 📊 Evaluation metrics
        metrics = evaluate(y_test, pred)

        # 🔝 Latest row
        latest = df.iloc[-1]

        # =========================
        # 🧠 INSIGHTS CALCULATION
        # =========================
        current_price = float(latest["Price"])
        mean_price = df["Price"].mean()

        trend = "Uptrend" if current_price > mean_price else "Downtrend"

        volatility_value = df["Price"].pct_change().std() * 100
        avg_return = df["Price"].pct_change().mean() * 100

        forecast_direction = "Up" if pred[-1] > current_price else "Down"

        signal = "BUY" if forecast_direction == "Up" and trend == "Uptrend" else "SELL"

        # =========================
        # 🚀 FINAL RESPONSE
        # =========================
        return jsonify({
            "ticker": ticker,

            # 🔝 SUMMARY
            "summary": {
                "price": current_price,
                "change_pct": float(latest.get("Change_pct", 0)),
                "volume": float(latest.get("Volume", 0)),
                "high_52w": float(df["Price"].max()),
                "low_52w": float(df["Price"].min())
            },

            # 🧠 INSIGHTS
            "insights": {
                "trend": trend,
                "volatility": float(volatility_value),
                "avg_return": float(avg_return),
                "forecast_direction": forecast_direction,
                "signal": signal
            },

            # 📊 CHART DATA (last 120 points)
            "chart": {
                "dates": df["Date"].astype(str).tolist()[-120:],
                "price": df["Price"].tolist()[-120:],
                "ma10": df["MA10"].fillna(0).tolist()[-120:],
                "ma20": df["MA20"].fillna(0).tolist()[-120:]
            },

            # 📉 VOLATILITY SERIES
            "volatility_series": df["Volatility"].fillna(0).tolist()[-120:],

            # 🔮 FORECAST
            "forecast": {
                "model": model,
                "metrics": metrics,
                "predictions": pred.tolist()
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500