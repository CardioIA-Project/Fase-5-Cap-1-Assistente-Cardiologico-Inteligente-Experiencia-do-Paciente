from flask import Flask
from flask_cors import CORS

from config import Config


def create_app():
    """Application factory: cria e configura a instância do Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Libera CORS pra interface (HTML/React Native) conseguir chamar a API
    CORS(app)

    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app