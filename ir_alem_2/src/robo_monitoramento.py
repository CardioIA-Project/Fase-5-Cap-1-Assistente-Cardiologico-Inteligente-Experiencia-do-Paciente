import argparse
import sqlite3
import sys
import traceback
import uuid
from datetime import datetime

import pandas as pd
import schedule
from pymongo import MongoClient
from sklearn.ensemble import IsolationForest

import config

sys.path.insert(0, f"{config.BASE_DIR}/db")
from mongo_setup import garantir_indices  # noqa: E402


def conectar_sqlite():
    conn = sqlite3.connect(config.SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def conectar_mongo():
    cliente = MongoClient(config.MONGO_URI)
    return cliente, garantir_indices(cliente)


def interpretar_mensagens_texto(mongo_db, execucao_id):
    """Varre mensagens pendentes e sinaliza as que citam termos de alerta.

    Propositalmente simples (casamento de substring, sem chamar um LLM):
    o robô roda em ciclo curto e frequente, então usar um modelo de
    linguagem completo (como o Chain-of-Thought do Ir Além 1) a cada
    execução seria caro e lento. Esta camada funciona como uma triagem
    rápida; casos sinalizados aqui são candidatos naturais para uma
    análise mais profunda com LLM, se um humano quiser investigar.
    """
    colecao = mongo_db["mensagens_pacientes"]
    pendentes = list(colecao.find({"processado_robo": False}))

    alertas_gerados = []
    for msg in pendentes:
        texto_normalizado = msg["texto"].lower()
        termos_encontrados = [
            termo for termo in config.TERMOS_ALERTA_TEXTO
            if termo in texto_normalizado
        ]
        sinalizado = len(termos_encontrados) > 0

        colecao.update_one(
            {"_id": msg["_id"]},
            {"$set": {
                "processado_robo": True,
                "sinalizado_ia": sinalizado,
                "termos_identificados": termos_encontrados,
            }},
        )

        if sinalizado:
            alertas_gerados.append({
                "execucao_id": execucao_id,
                "paciente_id": msg["paciente_id"],
                "timestamp": datetime.now(),
                "origem": "mensagem_texto",
                "motivo": f"Termo(s) de alerta identificado(s) no relato do paciente: "
                          f"{', '.join(termos_encontrados)}",
                "score_anomalia": None,
                "dados": {
                    "mensagem_id": str(msg["_id"]),
                    "texto": msg["texto"],
                    "termos_identificados": termos_encontrados,
                },
            })

    return len(pendentes), alertas_gerados


def avaliar_regras_fixas(df):
    """Aplica limiares clínicos fixos, mesma lógica da Action "Relatar
    sintoma" da Parte 1, adaptada de sintomas categóricos para valores
    numéricos contínuos."""
    lim = config.LIMIARES

    condicao = (
        (df["pressao_sistolica"] >= lim["pressao_sistolica_alta"]) |
        (df["pressao_sistolica"] <= lim["pressao_sistolica_baixa"]) |
        (df["pressao_diastolica"] >= lim["pressao_diastolica_alta"]) |
        (df["pressao_diastolica"] <= lim["pressao_diastolica_baixa"]) |
        (df["frequencia_cardiaca"] >= lim["frequencia_cardiaca_alta"]) |
        (df["frequencia_cardiaca"] <= lim["frequencia_cardiaca_baixa"]) |
        (df["adesao_tratamento_pct"] <= lim["adesao_tratamento_minima"])
    )
    df = df.copy()
    df["alerta_regra"] = condicao.astype(int)
    return df


def motivo_regra_fixa(row):
    lim = config.LIMIARES
    motivos = []
    if row["pressao_sistolica"] >= lim["pressao_sistolica_alta"]:
        motivos.append(f"pressão sistólica muito alta ({row['pressao_sistolica']} mmHg)")
    if row["pressao_sistolica"] <= lim["pressao_sistolica_baixa"]:
        motivos.append(f"pressão sistólica muito baixa ({row['pressao_sistolica']} mmHg)")
    if row["pressao_diastolica"] >= lim["pressao_diastolica_alta"]:
        motivos.append(f"pressão diastólica muito alta ({row['pressao_diastolica']} mmHg)")
    if row["pressao_diastolica"] <= lim["pressao_diastolica_baixa"]:
        motivos.append(f"pressão diastólica muito baixa ({row['pressao_diastolica']} mmHg)")
    if row["frequencia_cardiaca"] >= lim["frequencia_cardiaca_alta"]:
        motivos.append(f"frequência cardíaca muito alta ({row['frequencia_cardiaca']} bpm)")
    if row["frequencia_cardiaca"] <= lim["frequencia_cardiaca_baixa"]:
        motivos.append(f"frequência cardíaca muito baixa ({row['frequencia_cardiaca']} bpm)")
    if row["adesao_tratamento_pct"] <= lim["adesao_tratamento_minima"]:
        motivos.append(f"baixa adesão ao tratamento ({row['adesao_tratamento_pct']}%)")
    return "; ".join(motivos)


FEATURES = ["pressao_sistolica", "pressao_diastolica",
            "frequencia_cardiaca", "adesao_tratamento_pct"]


def aplicar_isolation_forest(conn, df_pendente):
    historico = pd.read_sql("SELECT * FROM sinais_vitais", conn)

    if len(historico) < config.IFOREST_MIN_HISTORICO:
        df_pendente = df_pendente.copy()
        df_pendente["anomalia_ia"] = None
        df_pendente["anomalia_score"] = None
        return df_pendente

    modelo = IsolationForest(
        contamination=config.IFOREST_CONTAMINATION,
        random_state=42,
    )
    modelo.fit(historico[FEATURES])

    df_pendente = df_pendente.copy()
    predicoes = modelo.predict(df_pendente[FEATURES])
    scores = modelo.decision_function(df_pendente[FEATURES])

    df_pendente["anomalia_ia"] = (predicoes == -1).astype(int)
    df_pendente["anomalia_score"] = scores
    return df_pendente


def executar_ciclo(mongo_db=None, cliente_mongo=None):
    execucao_id = str(uuid.uuid4())
    inicio = datetime.now()
    status, detalhes_erro = "sucesso", None
    leituras_avaliadas = mensagens_avaliadas = alertas_gerados_total = 0

    fechar_mongo_ao_final = mongo_db is None
    if mongo_db is None:
        cliente_mongo, mongo_db = conectar_mongo()

    conn = conectar_sqlite()
    todos_alertas = []

    try:
        mensagens_avaliadas, alertas_texto = interpretar_mensagens_texto(mongo_db, execucao_id)
        todos_alertas.extend(alertas_texto)

        df_pendente = pd.read_sql(
            "SELECT * FROM sinais_vitais WHERE processado_robo = 0", conn
        )
        leituras_avaliadas = len(df_pendente)

        if leituras_avaliadas > 0:
            df_pendente = avaliar_regras_fixas(df_pendente)
            df_pendente = aplicar_isolation_forest(conn, df_pendente)

            cur = conn.cursor()
            for _, row in df_pendente.iterrows():
                cur.execute(
                    """UPDATE sinais_vitais
                       SET processado_robo = 1, alerta_regra = ?,
                           anomalia_ia = ?, anomalia_score = ?
                       WHERE id = ?""",
                    (int(row["alerta_regra"]),
                     None if pd.isna(row["anomalia_ia"]) else int(row["anomalia_ia"]),
                     None if pd.isna(row["anomalia_score"]) else float(row["anomalia_score"]),
                     int(row["id"])),
                )

                if row["alerta_regra"] == 1:
                    todos_alertas.append({
                        "execucao_id": execucao_id,
                        "paciente_id": int(row["paciente_id"]),
                        "timestamp": datetime.now(),
                        "origem": "regra_fixa",
                        "motivo": motivo_regra_fixa(row),
                        "score_anomalia": None,
                        "dados": {
                            "sinal_vital_id": int(row["id"]),
                            "pressao_sistolica": int(row["pressao_sistolica"]),
                            "pressao_diastolica": int(row["pressao_diastolica"]),
                            "frequencia_cardiaca": int(row["frequencia_cardiaca"]),
                            "adesao_tratamento_pct": float(row["adesao_tratamento_pct"]),
                        },
                    })
                elif row.get("anomalia_ia") == 1:
                    todos_alertas.append({
                        "execucao_id": execucao_id,
                        "paciente_id": int(row["paciente_id"]),
                        "timestamp": datetime.now(),
                        "origem": "isolation_forest",
                        "motivo": "Combinação atípica de sinais vitais detectada pelo "
                                  "modelo (não capturada pelas regras fixas)",
                        "score_anomalia": float(row["anomalia_score"]),
                        "dados": {
                            "sinal_vital_id": int(row["id"]),
                            "pressao_sistolica": int(row["pressao_sistolica"]),
                            "pressao_diastolica": int(row["pressao_diastolica"]),
                            "frequencia_cardiaca": int(row["frequencia_cardiaca"]),
                            "adesao_tratamento_pct": float(row["adesao_tratamento_pct"]),
                        },
                    })

            conn.commit()

        if todos_alertas:
            mongo_db["alertas"].insert_many(todos_alertas)
        alertas_gerados_total = len(todos_alertas)

    except Exception:
        status = "erro"
        detalhes_erro = traceback.format_exc()
        conn.rollback()

    finally:
        fim = datetime.now()
        log = {
            "execucao_id": execucao_id,
            "inicio": inicio,
            "fim": fim,
            "duracao_segundos": (fim - inicio).total_seconds(),
            "leituras_avaliadas": leituras_avaliadas,
            "mensagens_avaliadas": mensagens_avaliadas,
            "alertas_gerados": alertas_gerados_total,
            "status": status,
            "detalhes_erro": detalhes_erro,
        }
        mongo_db["logs_execucao"].insert_one(log)
        conn.close()
        if fechar_mongo_ao_final and cliente_mongo:
            cliente_mongo.close()

    print(f"[{inicio:%H:%M:%S}] execução {execucao_id[:8]} — status={status} "
          f"| leituras={leituras_avaliadas} mensagens={mensagens_avaliadas} "
          f"alertas={alertas_gerados_total}")
    return log


def main():
    parser = argparse.ArgumentParser(description="Robô de monitoramento cardiológico (RPA)")
    parser.add_argument("--once", action="store_true",
                         help="roda um único ciclo e encerra (bom para testes/demo)")
    parser.add_argument("--intervalo", type=int, default=60,
                         help="segundos entre ciclos no modo contínuo (padrão: 60)")
    args = parser.parse_args()

    if args.once:
        executar_ciclo()
        return

    print(f"Robô iniciado — executando a cada {args.intervalo}s. Ctrl+C para parar.")
    schedule.every(args.intervalo).seconds.do(executar_ciclo)
    executar_ciclo()  # primeira execução imediata
    while True:
        schedule.run_pending()
        import time
        time.sleep(1)


if __name__ == "__main__":
    main()
