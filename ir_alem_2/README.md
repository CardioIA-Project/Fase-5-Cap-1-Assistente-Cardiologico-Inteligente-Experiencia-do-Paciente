# Ir Além 2 — Automação Inteligente com RPA, IA e Dados Híbridos

Módulo de monitoramento automatizado que expande o Assistente Cardiológico
(Parte 1 e Ir Além 1) com um robô de RPA que combina um banco relacional
(SQLite) e um banco não relacional (MongoDB) para monitorar sinais vitais
simulados, interpretar mensagens de texto de pacientes e registrar alertas
rastreáveis.

## Estrutura do projeto

```
ir_alem_2/
├── db/
│   ├── schema_sqlite.sql       # DDL do banco relacional
│   ├── mongo_schema.md         # documentação das coleções do MongoDB
│   └── mongo_setup.py          # cria coleções/índices no Mongo (idempotente)
├── src/
│   ├── config.py                # conexões, limiares e termos de alerta
│   ├── gerar_dados_simulados.py # popula pacientes, histórico e mensagens
│   └── robo_monitoramento.py    # ROBÔ — script principal da automação
├── notebooks/
│   └── analise_resultados.ipynb # visualização dos resultados (opcional)
└── relatorio_tecnico_ir_alem_2.pdf
```

## Pré-requisitos

- Python 3.10+
- MongoDB rodando localmente (`mongodb://localhost:27017`) — pode ser
  inspecionado com o MongoDB Compass
- Bibliotecas Python:

```bash
pip install pandas scikit-learn pymongo schedule
```

(Para rodar o notebook de análise, adicione `matplotlib seaborn jupyter`.)

## Como rodar

**1. Gerar os dados simulados** (uma única vez — cria `db/clinica.db` e
popula a coleção `mensagens_pacientes` no Mongo):

```bash
cd ir_alem_2
python src/gerar_dados_simulados.py
```

**2. Rodar o robô uma vez** (bom para testar/demonstrar):

```bash
python src/robo_monitoramento.py --once
```

**3. Ou rodar em modo contínuo**, simulando a automação periódica real
(a cada 60 segundos, por exemplo):

```bash
python src/robo_monitoramento.py --intervalo 60
```

Cada execução imprime um resumo no terminal e grava, no MongoDB:

- um documento em `logs_execucao` (metadados/rastreabilidade do ciclo);
- um documento em `alertas` para cada situação identificada, com a origem
  (`regra_fixa`, `isolation_forest` ou `mensagem_texto`).

E, no SQLite, atualiza cada leitura processada com seus rótulos
(`alerta_regra`, `anomalia_ia`, `anomalia_score`).

**4. (Opcional) Explorar os resultados** com o notebook em
`notebooks/analise_resultados.ipynb`, que lê os dois bancos e gera os
gráficos de dispersão e de alertas por paciente.

## Simulando novos dados ao longo do tempo

Para testar o robô continuamente sem esperar dias reais, rode
`gerar_dados_simulados.py` novamente após apagar `db/clinica.db` (isso
gera um novo lote de leituras "pendentes"), ou insira manualmente novas
linhas com `processado_robo = 0` na tabela `sinais_vitais` / novos
documentos com `processado_robo: false` na coleção `mensagens_pacientes`.
