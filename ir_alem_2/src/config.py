"""
Configurações compartilhadas do projeto Ir Além 2.

Centralizar aqui os caminhos/strings de conexão evita duplicação nos
outros módulos e facilita trocar, por exemplo, o host do MongoDB caso
o Compass esteja apontando para outra porta.
"""

import os

# --- SQLite (banco relacional) ---------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_PATH = os.path.join(BASE_DIR, "db", "clinica.db")

# --- MongoDB (banco não relacional) -----------------------------------
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "assistente_cardiologico"

# --- Critérios de alerta (mesmos da Parte 1 / Ir Além 1) --------------
# Sintomas textuais considerados sinal de alerta cardíaco.
TERMOS_ALERTA_TEXTO = [
    "dor no peito", "dor torácica", "aperto no peito",
    "falta de ar", "falta de ar intensa",
    "dor no braço", "dor irradiando", "dor no braço esquerdo",
    "suor frio", "sudorese fria",
]

# Limiares fixos para os sinais vitais estruturados.
# Valores simplificados para fins didáticos (não são recomendação médica).
LIMIARES = {
    "pressao_sistolica_alta": 180,
    "pressao_sistolica_baixa": 90,
    "pressao_diastolica_alta": 120,
    "pressao_diastolica_baixa": 60,
    "frequencia_cardiaca_alta": 120,
    "frequencia_cardiaca_baixa": 40,
    "adesao_tratamento_minima": 50.0,
}

# Contaminação esperada para o IsolationForest (mesmo valor usado no
# pipeline de exemplo da aula: contamination=0.08).
IFOREST_CONTAMINATION = 0.08
IFOREST_MIN_HISTORICO = 20  # nº mínimo de leituras para treinar o modelo
