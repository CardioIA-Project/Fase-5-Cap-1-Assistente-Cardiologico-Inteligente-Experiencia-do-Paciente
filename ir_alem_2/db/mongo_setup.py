"""
Cria (de forma idempotente) as coleções e índices do banco não relacional.

Pode ser rodado isoladamente:

    python db/mongo_setup.py

Ou importado — `robo_monitoramento.py` chama `garantir_indices()` no início
de cada execução, então rodar isso manualmente é opcional (mas ajuda a
inspecionar rapidamente a estrutura no Compass antes de rodar o robô).
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import config  # noqa: E402

from pymongo import MongoClient, ASCENDING, DESCENDING


def garantir_indices(cliente=None):
    fechar_ao_final = cliente is None
    cliente = cliente or MongoClient(config.MONGO_URI)
    mongo_db = cliente[config.MONGO_DB_NAME]

    mongo_db["mensagens_pacientes"].create_index(
        [("processado_robo", ASCENDING)], name="idx_mensagens_pendentes"
    )

    mongo_db["alertas"].create_index(
        [("paciente_id", ASCENDING), ("timestamp", DESCENDING)],
        name="idx_alertas_paciente_tempo",
    )
    mongo_db["alertas"].create_index(
        [("execucao_id", ASCENDING)], name="idx_alertas_execucao"
    )

    mongo_db["logs_execucao"].create_index(
        [("inicio", DESCENDING)], name="idx_logs_inicio"
    )

    if fechar_ao_final:
        cliente.close()

    return mongo_db


if __name__ == "__main__":
    db = garantir_indices()
    print(f"Banco '{config.MONGO_DB_NAME}' pronto. Coleções: {db.list_collection_names()}")
