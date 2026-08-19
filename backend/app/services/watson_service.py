from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class WatsonAssistantService:
    """
    Encapsula toda a comunicação com o IBM Watson Assistant (API v2).

    Responsabilidades:
    - Abrir/encerrar sessões de conversa
    - Enviar mensagens do usuário e extrair as respostas de texto
      do formato de resposta do Watson (que pode conter vários
      tipos de "response_type": text, option, image, etc.)

    Isolar isso aqui evita que as rotas do Flask precisem saber
    como o Watson estrutura suas respostas.
    """

    def __init__(self, api_key: str, url: str, assistant_id: str, version: str):
        authenticator = IAMAuthenticator(api_key)
        self.assistant = AssistantV2(version=version, authenticator=authenticator)
        self.assistant.set_service_url(url)
        self.assistant_id = assistant_id

    def create_session(self) -> str:
        """Cria uma nova sessão de conversa e retorna o session_id."""
        response = self.assistant.create_session(
            assistant_id=self.assistant_id
        ).get_result()
        return response["session_id"]

    def send_message(self, session_id: str, text: str) -> list[str]:
        """
        Envia uma mensagem de texto do usuário e retorna a lista de
        respostas em texto geradas pelo assistant.

        O Watson pode devolver blocos de tipos diferentes em
        output.generic, dependendo de como o step foi configurado:
        - "text": uma mensagem de texto simples (ex: o resumo final)
        - "option": uma pergunta com uma lista de opções pra escolher
          (é o que a maioria dos nossos steps usa, via "Define customer
          response" > Options)

        Como nosso frontend ainda é um chat simples de texto, a gente
        converte as opções em texto legível (título + lista numerada)
        em vez de simplesmente ignorá-las.
        """
        response = self.assistant.message(
            assistant_id=self.assistant_id,
            session_id=session_id,
            input={
                "message_type": "text",
                "text": text,
            },
        ).get_result()

        generic_items = response.get("output", {}).get("generic", [])
        replies = []

        for item in generic_items:
            response_type = item.get("response_type")

            if response_type == "text" and item.get("text"):
                replies.append(item["text"])

            elif response_type == "option":
                title = item.get("title", "")
                options = item.get("options", [])
                option_lines = [
                    f"- {opt.get('label')}" for opt in options if opt.get("label")
                ]
                option_block = "\n".join([title] + option_lines) if title else "\n".join(option_lines)
                if option_block:
                    replies.append(option_block)

        return replies

    def delete_session(self, session_id: str) -> None:
        """Encerra a sessão de conversa no Watson."""
        self.assistant.delete_session(
            assistant_id=self.assistant_id, session_id=session_id
        )
