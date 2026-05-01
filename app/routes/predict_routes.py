# from flask import Blueprint, request, jsonify
# from app.config import CSV_FILES
# from app.models.predictive_model import run_predictive_model

# predict_bp = Blueprint("predict", __name__)

# @predict_bp.route("/predict-model", methods=["GET"])
# def predict_model():

#     ticker = request.args.get("ticker")

#     if not ticker:
#         return jsonify({"error": "Ticker is required"}), 400

#     ticker = ticker.upper()

#     if ticker not in CSV_FILES:
#         return jsonify({"error": f"{ticker} not found"}), 404

#     try:
#         file_path = CSV_FILES[ticker]

#         predictions = run_predictive_model(file_path)

#         return jsonify({
#             "ticker": ticker,
#             "model": "custom_predictive_model",
#             "predictions": predictions
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



from flask import Blueprint, request, jsonify
from app.config import CSV_FILES
from app.models.ensemble import run_all_models

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict-model", methods=["GET"])
def predict_model():

    try:
        ticker = request.args.get("ticker")

        # ✅ validate input early
        if not ticker:
            return jsonify({"error": "Ticker is required"}), 400

        ticker = ticker.upper().strip()

        # ✅ validate ticker
        if ticker not in CSV_FILES:
            return jsonify({"error": f"{ticker} not found"}), 404

        file_path = CSV_FILES[ticker]

        # 🔥 run models
        results = run_all_models(file_path)

        return jsonify({
            "success": True,
            "ticker": ticker,
            "models": results
        })

    except Exception as e:
        # better debugging
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500