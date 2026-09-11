-- =====================================================================
-- Ir Além 2 — Esquema do banco relacional (SQLite)
-- Assistente Cardiológico — módulo de monitoramento automatizado (RPA)
-- =====================================================================
-- Este banco guarda os dados CLÍNICOS ESTRUTURADOS do paciente.
-- Logs de execução do robô, mensagens de texto e metadados ficam no
-- MongoDB (ver db/mongo_schema.md) — a divisão de responsabilidade
-- entre os dois bancos é justificada no relatório técnico, seção 3.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- Tabela: pacientes
-- Cadastro básico do paciente monitorado remotamente.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pacientes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    idade               INTEGER NOT NULL,
    fatores_risco       TEXT,        -- texto livre, mesmo padrão da Parte 1
                                      -- (ex.: "hipertensao, tabagismo")
    criado_em           TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------
-- Tabela: sinais_vitais
-- Leituras periódicas simuladas (pressão arterial, frequência cardíaca
-- e adesão ao tratamento). É sobre esta tabela que o robô de RPA atua.
--
-- As colunas `processado_robo`, `alerta_regra`, `anomalia_ia` e
-- `anomalia_score` funcionam como o "cartão de controle" do robô:
-- permitem que cada execução saiba exatamente quais leituras já foram
-- avaliadas e com qual resultado — o mesmo papel de tabela de
-- rastreabilidade/governança descrito na aula para a tabela
-- `validacao_execucoes`.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sinais_vitais (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id             INTEGER NOT NULL,
    timestamp               TEXT NOT NULL DEFAULT (datetime('now')),

    pressao_sistolica       INTEGER NOT NULL,   -- mmHg
    pressao_diastolica      INTEGER NOT NULL,   -- mmHg
    frequencia_cardiaca     INTEGER NOT NULL,   -- bpm
    adesao_tratamento_pct   REAL    NOT NULL,   -- % de doses tomadas (0-100)

    -- --- controle do robô (preenchido pela automação, não na inserção) ---
    processado_robo         INTEGER NOT NULL DEFAULT 0,   -- 0/1
    alerta_regra            INTEGER NOT NULL DEFAULT 0,   -- 0/1 (regra fixa)
    anomalia_ia             INTEGER,                      -- 0/1 (IsolationForest)
    anomalia_score          REAL,                         -- decision_function

    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

CREATE INDEX IF NOT EXISTS idx_sinais_pendentes
    ON sinais_vitais (processado_robo);

CREATE INDEX IF NOT EXISTS idx_sinais_paciente
    ON sinais_vitais (paciente_id, timestamp);
