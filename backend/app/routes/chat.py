from flask import Blueprint, request, jsonify, current_app

from app.services.watson_service import WatsonAssistantService

chat_bp = Blueprint("chat", __name__, url_prefix="/api")

# Instância única do serviço, criada sob demanda (lazy init) na primeira
# requisição — evita erro na subida do app se o .env ainda não tiver
# sido preenchido durante o desenvolvimento local.
_watson_service: WatsonAssistantService | None = None


def get_watson_service() -> WatsonAssistantService:
    global _watson_service
    if _watson_service is None:
        cfg = current_app.config
        _watson_service = WatsonAssistantService(
            api_key=cfg["WATSON_API_KEY"],
            url=cfg["WATSON_URL"],
            assistant_id=cfg["WATSON_ASSISTANT_ID"],
            version=cfg["WATSON_VERSION"],
        )
    return _watson_service


@chat_bp.route("/session", methods=["POST"])
def start_session():
    """Abre uma nova sessão de conversa com o Watson Assistant."""
    try:
        service = get_watson_service()
        session_id = service.create_session()
        return jsonify({"session_id": session_id})
    except Exception as e:
        return jsonify({"error": f"Falha ao criar sessão: {str(e)}"}), 500


@chat_bp.route("/message", methods=["POST"])
def send_message():
    """
    Recebe { session_id, text } do frontend, repassa pro Watson
    e retorna { replies: [...] } com as respostas do assistant.
    """
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    text = data.get("text")

    if not session_id or not text:
        return jsonify({"error": "Campos 'session_id' e 'text' são obrigatórios"}), 400

    try:
        service = get_watson_service()
        replies = service.send_message(session_id, text)
        return jsonify({"replies": replies})
    except Exception as e:
        return jsonify({"error": f"Falha ao enviar mensagem: {str(e)}"}), 500


@chat_bp.route("/session/<session_id>", methods=["DELETE"])
def end_session(session_id):
    """Encerra a sessão de conversa (chamado quando o usuário sai do chat)."""
    try:
        service = get_watson_service()
        service.delete_session(session_id)
        return jsonify({"status": "session encerrada"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500