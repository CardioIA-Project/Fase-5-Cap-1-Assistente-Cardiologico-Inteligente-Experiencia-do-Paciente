# Estrutura do banco não relacional (MongoDB)

Banco: `assistente_cardiologico` — acessado localmente via `mongodb://localhost:27017`
(mesma instância visível no MongoDB Compass).

Diferente do SQLite, o MongoDB é **schemaless**: não há um `CREATE TABLE` a
declarar antecipadamente. Por isso, em vez de DDL, este arquivo documenta a
**forma esperada dos documentos** de cada coleção — o "contrato" que o
código em `src/robo_monitoramento.py` segue ao gravar e ler dados. O script
`db/mongo_setup.py` cria as coleções, os índices e (opcionalmente) um
*schema validator* do MongoDB que reforça esse contrato no servidor.

Justificativa de projeto: as três coleções abaixo guardam informação com
formato **variável e principalmente textual/de auditoria** (logs, mensagens
livres de pacientes, alertas com origens diferentes) — exatamente o cenário
em que o resumo da aula aponta o NoSQL como mais adequado que o modelo
relacional rígido, ao custo de uma consistência mais "eventual" no lugar das
garantias ACID do SQLite (trade-off aceitável aqui, pois nenhuma dessas
coleções participa de uma transação financeira ou clínica crítica — elas são
o *rastro* da automação, não a fonte de verdade dos sinais vitais, que
permanece no SQLite).

---

## Coleção `logs_execucao`

Um documento por **ciclo de execução do robô** (rastreabilidade do processo
de RPA em si).

```json
{
  "_id": ObjectId("..."),
  "execucao_id": "b3f1c2a0-...-uuid4",
  "inicio": ISODate("2026-09-09T12:00:00Z"),
  "fim": ISODate("2026-09-09T12:00:04Z"),
  "duracao_segundos": 4.21,
  "leituras_avaliadas": 12,
  "mensagens_avaliadas": 3,
  "alertas_gerados": 2,
  "status": "sucesso",           // "sucesso" | "erro"
  "detalhes_erro": null           // string com o traceback, se status = "erro"
}
```

## Coleção `mensagens_pacientes`

Mensagens de texto livre simuladas (ex.: relato de sintoma pelo app/canal de
adesão). O robô interpreta essas mensagens com uma técnica simples de
casamento de palavras-chave (ver relatório, seção 4.3).

```json
{
  "_id": ObjectId("..."),
  "paciente_id": 3,
  "timestamp": ISODate("2026-09-09T11:58:00Z"),
  "canal": "app_adesao",
  "texto": "Hoje senti um leve aperto no peito depois da caminhada...",
  "processado_robo": true,
  "sinalizado_ia": true,
  "termos_identificados": ["aperto no peito"]
}
```

## Coleção `alertas`

Evento de alerta **normalizado**, não importa a origem (regra fixa,
IsolationForest ou texto). É a coleção que garante rastreabilidade
ponta-a-ponta: qualquer alerta pode ser rastreado até a execução do robô
que o gerou (`execucao_id`) e até o dado bruto que o motivou (`dados`).

```json
{
  "_id": ObjectId("..."),
  "execucao_id": "b3f1c2a0-...-uuid4",
  "paciente_id": 3,
  "timestamp": ISODate("2026-09-09T12:00:02Z"),
  "origem": "isolation_forest",     // "regra_fixa" | "isolation_forest" | "mensagem_texto"
  "motivo": "Padrão anômalo de pressão/frequência não capturado pelas regras fixas",
  "score_anomalia": -0.14,          // presente apenas quando origem = isolation_forest
  "dados": {                        // snapshot do que motivou o alerta
    "sinal_vital_id": 128,
    "pressao_sistolica": 176,
    "pressao_diastolica": 96,
    "frequencia_cardiaca": 118,
    "adesao_tratamento_pct": 42.0
  }
}
```

---

## Índices criados por `mongo_setup.py`

| Coleção               | Índice                              | Motivo                                   |
|-----------------------|--------------------------------------|-------------------------------------------|
| `mensagens_pacientes` | `processado_robo`                   | robô varre só as mensagens pendentes       |
| `alertas`             | `paciente_id`, `timestamp` (composto)| consulta rápida do histórico de um paciente|
| `alertas`             | `execucao_id`                        | rastreabilidade: todos os alertas de um ciclo |
| `logs_execucao`       | `inicio` (descendente)                | ver execuções mais recentes primeiro       |
