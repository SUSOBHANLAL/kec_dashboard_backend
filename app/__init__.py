# # from flask import Flask
# # from app.routes.forecast_routes import forecast_bp

# def create_app():
#     app = Flask(__name__)

#     # Register Blueprints
#     app.register_blueprint(forecast_bp, url_prefix="/api/v1")

#     @app.route("/")
#     def home():
#         return {"status": "ok", "message": "Flask API running"}

#     return app

# # from flask import Flask
# # from flask_cors import CORS

# # from app.routes.forecast_routes import forecast_bp

# # app = Flask(__name__)

# # # 🔥 ENABLE CORS
# # CORS(app)

# # app.register_blueprint(forecast_bp, url_prefix="/api/v1")

# # if __name__ == "__main__":
# #     app.run(debug=True)




# from flask import Flask
# from flask_cors import CORS

# from app.routes.forecast_routes import forecast_bp

# app = Flask(__name__)

# # Enable CORS
# CORS(app)

# # Register routes
# app.register_blueprint(forecast_bp, url_prefix="/api/v1")

# @app.route("/")
# def home():
#     return {"status": "ok", "message": "Flask API running"}

# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask
from flask_cors import CORS

from app.routes.forecast_routes import forecast_bp
from app.routes.predict_routes import predict_bp
from app.routes.indicator_routes import indicator_bp


def create_app():
    app = Flask(__name__)

    # 🔥 Enable CORS properly
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register Blueprints
    app.register_blueprint(forecast_bp, url_prefix="/api/v1")

    app.register_blueprint(predict_bp, url_prefix="/api/v1")
    app.register_blueprint(indicator_bp, url_prefix="/api/v1")

    @app.route("/")
    def home():
        return {"status": "ok", "message": "Flask API running"}

    return app