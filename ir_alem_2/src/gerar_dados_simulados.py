import random
import sqlite3
from datetime import datetime, timedelta

from pymongo import MongoClient

import config

random.seed(42)

PACIENTES = [
    {"nome": "Ana Beatriz Souza",   "idade": 61, "fatores_risco": "hipertensao, sedentarismo"},
    {"nome": "Carlos Eduardo Lima", "idade": 54, "fatores_risco": "tabagismo, colesterol alto"},
    {"nome": "Marta Oliveira",      "idade": 68, "fatores_risco": "diabetes, hipertensao, obesidade"},
    {"nome": "João Pedro Alves",    "idade": 45, "fatores_risco": "historico familiar"},
    {"nome": "Fernanda Ribeiro",    "idade": 72, "fatores_risco": "diabetes, sedentarismo"},
]

MENSAGENS_TEMPLATE = [
    ("Hoje senti um leve aperto no peito depois da caminhada da tarde, passou em alguns minutos.", True),
    ("Estou tomando os remédios certinho, sem novidades essa semana.", False),
    ("Senti falta de ar subindo a escada de casa, tive que parar no meio.", True),
    ("Só um cansaço de fim de dia, nada muito diferente do normal.", False),
    ("Acordei de madrugada com suor frio e um desconforto forte no peito.", True),
    ("Esqueci de tomar o remédio da tarde, mas me sinto bem.", False),
    ("Notei um leve inchaço no tornozelo, sem dor.", False),
    ("Dor irradiando do peito para o braço esquerdo, começou agora há pouco.", True),
]


def criar_schema_sqlite(conn):
    with open(f"{config.BASE_DIR}/db/schema_sqlite.sql", encoding="utf-8") as f:
        conn.executescript(f.read())


def gerar_leitura(paciente_idx, forcar_anomalia=None):
    """Gera uma leitura de sinais vitais plausível para um paciente.

    forcar_anomalia:
        None         -> leitura normal (com variação natural)
        "regra"      -> viola um limiar fixo (ex.: pico hipertensivo)
        "sutil"      -> combinação atípica, mas dentro dos limiares fixos
                        (só o IsolationForest tende a capturar)
    """
    base_sistolica = 118 + paciente_idx * 3
    base_diastolica = 76 + paciente_idx * 2
    base_fc = 72 + paciente_idx * 2
    base_adesao = 88 - paciente_idx * 2

    if forcar_anomalia == "regra":
        return {
            "pressao_sistolica": random.choice([190, 200, 85]),
            "pressao_diastolica": random.choice([125, 58]),
            "frequencia_cardiaca": random.choice([135, 38]),
            "adesao_tratamento_pct": round(random.uniform(20, 45), 1),
        }

    if forcar_anomalia == "sutil":
        return {
            "pressao_sistolica": random.randint(150, 158),
            "pressao_diastolica": random.randint(95, 100),
            "frequencia_cardiaca": random.randint(105, 112),
            "adesao_tratamento_pct": round(random.uniform(55, 62), 1),
        }

    return {
        "pressao_sistolica": int(random.gauss(base_sistolica, 6)),
        "pressao_diastolica": int(random.gauss(base_diastolica, 4)),
        "frequencia_cardiaca": int(random.gauss(base_fc, 5)),
        "adesao_tratamento_pct": round(max(0, min(100, random.gauss(base_adesao, 6))), 1),
    }


def popular_sqlite():
    conn = sqlite3.connect(config.SQLITE_PATH)
    criar_schema_sqlite(conn)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM pacientes")
    if cur.fetchone()[0] > 0:
        print("SQLite já populado — pulando geração (apague db/clinica.db para recomeçar).")
        conn.close()
        return

    paciente_ids = []
    for p in PACIENTES:
        cur.execute(
            "INSERT INTO pacientes (nome, idade, fatores_risco) VALUES (?, ?, ?)",
            (p["nome"], p["idade"], p["fatores_risco"]),
        )
        paciente_ids.append(cur.lastrowid)

    agora = datetime.now()

    historico = []
    for dias_atras in range(60, 2, -1):
        ts = agora - timedelta(days=dias_atras, minutes=random.randint(0, 59))
        for idx, paciente_id in enumerate(paciente_ids):
            forcar = "sutil" if random.random() < 0.04 else None
            leitura = gerar_leitura(idx, forcar_anomalia=forcar)
            historico.append((
                paciente_id, ts.isoformat(sep=" ", timespec="seconds"),
                leitura["pressao_sistolica"], leitura["pressao_diastolica"],
                leitura["frequencia_cardiaca"], leitura["adesao_tratamento_pct"],
                1, 0, None, None,
            ))

    cur.executemany(
        """INSERT INTO sinais_vitais
           (paciente_id, timestamp, pressao_sistolica, pressao_diastolica,
            frequencia_cardiaca, adesao_tratamento_pct,
            processado_robo, alerta_regra, anomalia_ia, anomalia_score)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        historico,
    )

    novos = []
    padrao_do_lote = [None, None, "regra", None, "sutil", None, None, "regra", None, None, None, "sutil"]
    for i, forcar in enumerate(padrao_do_lote):
        idx = i % len(paciente_ids)
        ts = agora - timedelta(minutes=(len(padrao_do_lote) - i) * 5)
        leitura = gerar_leitura(idx, forcar_anomalia=forcar)
        novos.append((
            paciente_ids[idx], ts.isoformat(sep=" ", timespec="seconds"),
            leitura["pressao_sistolica"], leitura["pressao_diastolica"],
            leitura["frequencia_cardiaca"], leitura["adesao_tratamento_pct"],
            0, 0, None, None,
        ))

    cur.executemany(
        """INSERT INTO sinais_vitais
           (paciente_id, timestamp, pressao_sistolica, pressao_diastolica,
            frequencia_cardiaca, adesao_tratamento_pct,
            processado_robo, alerta_regra, anomalia_ia, anomalia_score)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        novos,
    )

    conn.commit()
    conn.close()
    print(f"SQLite populado: {len(paciente_ids)} pacientes, "
          f"{len(historico)} leituras históricas, {len(novos)} leituras pendentes.")
    return paciente_ids


def popular_mongo(paciente_ids):
    if paciente_ids is None:
        conn = sqlite3.connect(config.SQLITE_PATH)
        paciente_ids = [r[0] for r in conn.execute("SELECT id FROM pacientes").fetchall()]
        conn.close()

    cliente = MongoClient(config.MONGO_URI)
    mongo_db = cliente[config.MONGO_DB_NAME]
    colecao = mongo_db["mensagens_pacientes"]

    if colecao.count_documents({}) > 0:
        print("MongoDB já populado — pulando geração (limpe a coleção para recomeçar).")
        cliente.close()
        return

    agora = datetime.now()
    documentos = []
    for i, (texto, _tem_alerta) in enumerate(MENSAGENS_TEMPLATE):
        paciente_id = paciente_ids[i % len(paciente_ids)]
        documentos.append({
            "paciente_id": paciente_id,
            "timestamp": agora - timedelta(minutes=(len(MENSAGENS_TEMPLATE) - i) * 7),
            "canal": "app_adesao",
            "texto": texto,
            "processado_robo": False,
            "sinalizado_ia": None,
            "termos_identificados": [],
        })

    colecao.insert_many(documentos)
    cliente.close()
    print(f"MongoDB populado: {len(documentos)} mensagens de pacientes pendentes.")


if __name__ == "__main__":
    ids = popular_sqlite()
    popular_mongo(ids)
