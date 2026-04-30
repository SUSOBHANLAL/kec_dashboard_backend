from flask import Flask
from app.routes.forecast_routes import forecast_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(forecast_bp, url_prefix="/api/v1")

    @app.route("/")
    def home():
        return {"status": "ok", "message": "Flask API running"}

    return app