from flask import Flask


def create_app(config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SECRET_KEY"] = "weather-secret-key"
    app.config["OPENWEATHER_API_KEY"] = ""   # injected via env var in routes

    if config:
        app.config.update(config)

    from app.routes import main
    app.register_blueprint(main)

    return app
