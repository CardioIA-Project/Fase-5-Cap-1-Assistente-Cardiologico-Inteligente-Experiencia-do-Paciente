import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações centrais da aplicação, lidas do .env"""

    WATSON_API_KEY = os.getenv("WATSON_ASSISTANT_API_KEY")
    WATSON_URL = os.getenv("WATSON_ASSISTANT_URL")
    WATSON_ASSISTANT_ID = os.getenv("WATSON_ASSISTANT_ID")
    WATSON_VERSION = os.getenv("WATSON_ASSISTANT_VERSION", "2021-06-14")

    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"

    @classmethod
    def validate(cls):
        """Confere se as credenciais essenciais do Watson foram configuradas."""
        missing = [
            name
            for name, value in [
                ("WATSON_ASSISTANT_API_KEY", cls.WATSON_API_KEY),
                ("WATSON_ASSISTANT_URL", cls.WATSON_URL),
                ("WATSON_ASSISTANT_ID", cls.WATSON_ASSISTANT_ID),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(
                f"Variáveis de ambiente faltando no .env: {', '.join(missing)}"
            )