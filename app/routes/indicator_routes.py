from flask import Blueprint, request, jsonify
import pandas as pd

from app.config import CSV_FILES
from app.services.indicator_service import process_indicators

indicator_bp = Blueprint("indicator", __name__)


@indicator_bp.route("/indicators/<ticker>", methods=["GET"])
def indicators(ticker):

    ticker = ticker.upper()

    # ─────────────────────────────
    # CHECK TICKER VALIDITY
    # ─────────────────────────────
    if ticker not in CSV_FILES:
        return jsonify({"error": "Invalid ticker"}), 404

    # ─────────────────────────────
    # LOAD DATA + INDICATORS
    # ─────────────────────────────
    df = process_indicators(CSV_FILES[ticker])

    # ─────────────────────────────
    # NORMALIZE DATE
    # ─────────────────────────────
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.sort_values("Date")

    # ─────────────────────────────
    # GET QUERY PARAMS
    # ─────────────────────────────
    start_date = request.args.get("from")
    end_date = request.args.get("to")
    single_date = request.args.get("date")

    # ─────────────────────────────
    # CASE 1: SINGLE DATE (FIXED)
    # ─────────────────────────────
    if single_date:
        try:
            single_date = pd.to_datetime(single_date)

            # 🔥 ONLY PAST DATA (NO FUTURE BUG)
            past_df = df[df["Date"] <= single_date]

            if past_df.empty:
                return jsonify({
                    "error": "No historical data available before this date"
                }), 400

            # 🔥 GET LATEST AVAILABLE BEFORE DATE
            closest_date = past_df["Date"].max()
            df = df[past_df["Date"] == closest_date]

        except Exception:
            return jsonify({"error": "Invalid date format"}), 400

    # ─────────────────────────────
    # CASE 2: DATE RANGE FILTER
    # ─────────────────────────────
    else:

        if start_date:
            try:
                start_date = pd.to_datetime(start_date)
                df = df[df["Date"] >= start_date]
            except:
                return jsonify({"error": "Invalid 'from' date"}), 400

        if end_date:
            try:
                end_date = pd.to_datetime(end_date)
                df = df[df["Date"] <= end_date]
            except:
                return jsonify({"error": "Invalid 'to' date"}), 400

    # ─────────────────────────────
    # SAFETY CHECK
    # ─────────────────────────────
    if df.empty:
        return jsonify({
            "error": "No data found for selected date range/date"
        }), 400

    # ─────────────────────────────
    # BUY / SELL SIGNALS
    # ─────────────────────────────
    buy = df[df["Crossover"] == 1]
    sell = df[df["Crossover"] == -1]

    # ─────────────────────────────
    # RESPONSE
    # ─────────────────────────────
    return jsonify({
        "ticker": ticker,

        "date": df["Date"].astype(str).tolist(),
        "price": df["Price"].tolist(),

        "sma10": df["SMA10"].tolist(),
        "ema5": df["EMA5"].tolist(),
        "ema10": df["EMA10"].tolist(),

        "buy_signals": buy["Price"].tolist(),
        "sell_signals": sell["Price"].tolist()
    })