# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP" border="0" width="40%" height="40%"></a>
</p>

# 🫀 CardioIA — Assistente Conversacional Cardiológico

O **CardioIA** é um chatbot de saúde digital para triagem e orientação cardiológica inicial. A aplicação utiliza o **IBM watsonx Assistant** integrado a um backend robusto em **Python (Flask)** para interpretar mensagens em linguagem natural e fornecer orientação rápida e segura aos pacientes com base no contexto clínico informado.

---

## Integrantes

- <a href="https://github.com/Vitor985-hub">Vitor Eiji</a>
- <a href="https://github.com/BPilecarte">Beatriz Pilecarte</a>
- <a href="https://github.com/yggdrasilGit">Franciscmar Alves</a>
- <a href="https://github.com/matheusbento04">Matheus Soares</a>
- <a href="https://github.com/AntonioBarros19">Antonio Barros</a>

## Professores

### Tutor(a)

- <a href="https://www.linkedin.com/in/caique-nonato/">Caique Nonato</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">Andre Godoi Chiochiovatto</a>

---

## Visão Geral

O projeto **CardioIA** realiza a triagem inicial de sintomas cardiológicos através de Processamento de Linguagem Natural (NLP). 

> **Aviso Importante:** O assistente não realiza diagnósticos médicos. Seu propósito é coletar informações estruturadas sobre o sintoma relatado e orientar adequadamente o usuário — seja recomendando consulta médica de rotina, seja sinalizando casos de emergência.

### Principais Características e Funcionalidades

- **Triagem Prioritária de Emergência (Bifurcação Condicional):** Identifica imediatamente sinais de alerta críticos (*dor no peito, falta de ar, dor no braço, suor frio*) e interrompe o fluxo com orientações para acionar o SAMU (192) ou buscar um pronto-socorro.
- **Investigação de Sintomas Moderados/Leves:** Para sintomas não graves (*palpitação, tontura, cansaço, inchaço nas pernas*), investiga a severidade (leve, moderada, intensa), duração (minutos, horas, dias, semanas) e fatores de risco associados (hipertensão, diabetes, tabagismo, etc.).
- **Resumo Dinâmico do Quadro:** Reconstrói dinamicamente a síntese do relato ao final do fluxo com base nas variáveis da sessão.
- **Backend Flask Encapsulado:** Interface RESTful que isola credenciais de API (`.env`), gerencia sessões ativas e formata respostas legíveis (convertendo blocos do tipo `option` e `text` do Watson).

---

## Modelagem no IBM watsonx Assistant

A inteligência conversacional foi construída utilizando o modelo de **Actions** do watsonx Assistant.

- **Action Principal:** `Relatar sintoma`
- **Frases de Treinamento:** Treinada com múltiplos exemplos de relatos de sintomas cardiológicos.
- **Estrutura do Fluxo (6 Steps):**
  1. **Step 1:** Coleta do sintoma principal (entre 8 opções configuradas).
  2. **Step 2:** Verificação condicional de emergência (sinal de alerta aciona protocolo de emergência e encerra o atendimento).
  3. **Step 3:** Coleta do nível de severidade (para sintomas não críticos).
  4. **Step 4:** Coleta do tempo de duração do sintoma.
  5. **Step 5:** Coleta dos fatores de risco associados.
  6. **Step 6:** Apresentação do resumo final do paciente e recomendação de consulta com cardiologista.

A exportação oficial da Action configurada está disponível no repositório em `watson/Assistente-Cardiológico-Conversacional-action.json`.

---

## Extração Clínica e IA Generativa — Ir Além 1

A pasta [`ir_alem_1/`](ir_alem_1) contém a solução da atividade complementar **Ir Além 1**, que expande o assistente para interpretar e extrair informações de relatos clínicos não estruturados em formato JSON utilizando técnicas avançadas de engenharia de prompt.

### Conteúdo do Módulo
- **[`ir_alem_1/ir_alem_1_extracao_clinica.ipynb`](ir_alem_1/ir_alem_1_extracao_clinica.ipynb):** Jupyter Notebook interativo contendo todo o fluxo de extração, experimentos comparativos e validação de schema.
- **[`ir_alem_1/ir_alem_1.pdf`](ir_alem_1/ir_alem_1.pdf):** Relatório técnico detalhado com fundamentação do Chain of Thought, justificativa da troca para Ollama/llama3.1:8b, análise comparativa dos casos clínicos e conclusões.

### Abordagem Técnica e Destaques
- **Chain of Thought (CoT):** Em vez de solicitar diretamente se o paciente apresenta risco (comportamento "caixa-preta"), o prompt força o modelo a seguir passos explícitos de raciocínio:
  1. Identificação individualizada dos sintomas descritos.
  2. Comparação de cada sintoma com os critérios de alerta cardiológico (*dor no peito, falta de ar, dor no braço, suor frio*).
  3. Classificação final (booleana) acompanhada do resumo narrativo.
- **Validação de Schema com Pydantic:** Integração de validação programática da resposta em JSON com política de retry automático em caso de parsing inválido.
- **Execução via Ollama (`llama3.1:8b`):** Uso de modelo de linguagem local, demonstrando a portabilidade dos conceitos de prompting independentemente da plataforma ou LLM utilizada.
- **Análise Comparativa:** Comparação prática entre a inferência simples (*sem CoT*) e a inferência estruturada com justificativa (*com CoT*), ressaltando os benefícios em termos de transparência e auditabilidade clínica.

---

## Automação Inteligente com RPA, IA e Dados Híbridos — Ir Além 2

A pasta [`ir_alem_2/`](ir_alem_2) contém a solução da atividade complementar **Ir Além 2**, expandindo o ecossistema com um robô de Automação Robótica de Processos (RPA) integrado a técnicas de IA e dados híbridos (relacional + não relacional). O robô monitora continuamente pacientes simulados, detecta anomalias clínicas multivariadas e registra eventos auditáveis com rastreabilidade total.

### Conteúdo do Módulo
- **Robô de Automação (`ir_alem_2/src/robo_monitoramento.py`):** Script em Python que executa ciclos periódicos (ou sob demanda via `--once`), lendo dados pendentes, executando a inferência das IAs e persistindo decisões.
- **Banco Relacional (`ir_alem_2/db/schema_sqlite.sql`):** SQLite utilizado como fonte de verdade estruturada para cadastro de pacientes e histórico de sinais vitais (*pressão arterial sistólica/diastólica, frequência cardíaca, adesão ao tratamento*), com colunas de controle transacional ACID (`processado_robo`, `alerta_regra`, `anomalia_ia`, `anomalia_score`).
- **Banco Não Relacional (`ir_alem_2/db/mongo_schema.md`):** MongoDB documentado com 3 coleções:
  - `logs_execucao`: Rastreabilidade do ciclo do robô (início, fim, leituras avaliadas, status, erros).
  - `mensagens_pacientes`: Mensagens livres de pacientes em linguagem natural com sinalização de termos.
  - `alertas`: Eventos normalizados de alerta com chave de rastreio (`execucao_id` + `paciente_id`), motivo e snapshot dos dados clínicos no momento da detecção.
- **Setup e Dados Simulados (`ir_alem_2/src/gerar_dados_simulados.py`, `ir_alem_2/db/mongo_setup.py`):** Scripts para povoamento do banco relacional com dados sintéticos e configuração idempotente das coleções/índices no Mongo.
- **Notebook de Análise (`ir_alem_2/notebooks/analise_resultados.ipynb`):** Análise exploratória e visualização dos alertas e fronteiras do modelo.
- **Relatório Técnico (`ir_alem_2/relatorio_tecnico_ir_alem_2.pdf`):** Relatório detalhado (5 páginas) cobrindo decisões de arquitetura, governança, modelos estatísticos e rastreabilidade.

### Abordagem Técnica e Técnicas de IA
1. **Regras Fixas de Limiar Clínico (Baseline Determinístico):** Identificação imediata de valores críticos extremos (ex.: pressão sistólica ≥ 180 ou ≤ 90 mmHg, FC ≥ 120 ou ≤ 40 bpm, adesão ≤ 50%), garantindo respostas instantâneas para casos evidentes.
2. **Detecção de Anomalias Multivariadas (Isolation Forest):** Modelo de Machine Learning não supervisionado (`scikit-learn`, `contamination=0.08`) treinado sobre o histórico de dados vitais para identificar combinações atípicas sutis que não violam nenhum limiar fixo isoladamente.
3. **Casamento de Padrões em Mensagens de Texto:** Varredura ágil de mensagens de texto livre de pacientes contra termos de alerta cardiológico herdados do assistente.
4. **Governança e Rastreabilidade:** Cada ciclo recebe um `execucao_id` único (UUIDv4) compartilhado entre o SQLite e o MongoDB, permitindo reconstruir com precisão a cadeia causal de cada alerta gerado.

---

## Estrutura do Projeto

```text
.
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── chat.py               # Endpoints REST: /api/session, /api/message
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── watson_service.py     # Encapsulamento da SDK do IBM Assistant V2
│   │   └── __init__.py               # Factory da aplicação Flask com suporte a CORS
│   ├── config.py                     # Validação e carregamento de variáveis de ambiente (.env)
│   └── run.py                        # Ponto de entrada para execução da API
├── frontend/
│   ├── app/
│   │   ├── _layout.tsx               # Layout raiz (navegação Expo Router)
│   │   └── index.tsx                 # Tela principal da interface do chat (React Native)
│   ├── app.json                      # Configurações do app Expo
│   └── package.json                  # Dependências do frontend
├── docs/
│   └── relatorio_parte1.txt          # Relatório técnico completo da Parte 1
├── ir_alem_1/
│   ├── ir_alem_1.pdf                 # Relatório técnico com Chain of Thought e validação Pydantic
│   └── ir_alem_1_extracao_clinica.ipynb # Notebook com extração via CoT e LLM local (Ollama)
├── ir_alem_2/
│   ├── db/
│   │   ├── schema_sqlite.sql         # DDL do banco relacional (SQLite)
│   │   ├── mongo_schema.md           # Documentação das coleções do MongoDB
│   │   └── mongo_setup.py            # Setup idempotente de coleções e índices Mongo
│   ├── src/
│   │   ├── config.py                 # Configurações, conexões e limiares clínicos
│   │   ├── gerar_dados_simulados.py  # Popula pacientes, histórico e mensagens
│   │   └── robo_monitoramento.py     # Script principal do robô RPA (periódico ou pontual)
│   ├── notebooks/
│   │   └── analise_resultados.ipynb  # Visualização dos resultados e dispersões
│   ├── relatorio_tecnico_ir_alem_2.pdf # Relatório técnico completo do Ir Além 2
│   └── README.md                     # Guia específico do módulo Ir Além 2
├── watson/
│   └── Assistente-Cardiológico-Conversacional-action.json # Exportação oficial da Action do Watson
├── .env.example                      # Modelo das variáveis de ambiente necessárias
├── .gitignore                        # Regras de exclusão de arquivos temporários/segredos
├── requirements.txt                  # Dependências consolidadas (Backend, Ir Além 1 e Ir Além 2)
└── README.md                         # Documentação principal do repositório
```

---

## Endpoints da API Backend

A API Flask fornece os seguintes recursos na rota `/api`:

| Método | Endpoint | Descrição | Corpo da Requisição (Payload) | Resposta |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/session` | Cria uma nova sessão no Watson | *(Nenhum)* | `{ "session_id": "string" }` |
| `POST` | `/api/message` | Envia mensagem do usuário | `{ "session_id": "string", "text": "string" }` | `{ "replies": ["string"] }` |
| `DELETE` | `/api/session/<session_id>` | Encerra a sessão | *(Nenhum)* | `{ "status": "session encerrada" }` |
| `GET` | `/health` | Healthcheck da API | *(Nenhum)* | `{ "status": "ok" }` |

---

## Demonstração em Vídeo (Parte 2)

> 📹 **Link do Vídeo de Demonstração:** [Adicione aqui o link do vídeo do YouTube / Drive / Vimeo]
>
> Demonstração prática (até 3 minutos) evidenciando a inicialização da sessão, envio de mensagens em linguagem natural, apresentação das opções pelo assistente cardiológico e o acionamento do protocolo visual de emergência ao relatar sintomas críticos.

---

## Como Executar

### 1. Pré-requisitos Gerais
- **Python 3.10+** instalado.
- **Node.js 18+** e npm (para o frontend mobile).
- Instância ativa do **IBM watsonx Assistant** na IBM Cloud com a Action importada (`watson/Assistente-Cardiológico-Conversacional-action.json`).
- *(Para Ir Além 1)*: **Ollama** com o modelo `llama3.1:8b` (`ollama run llama3.1:8b`).
- *(Para Ir Além 2)*: Instância local do **MongoDB** ativa (`mongodb://localhost:27017`).

### 2. Clonar o Repositório
```bash
git clone https://github.com/Vitor985-hub/Fase-5-Cap-1-Assistente-Cardiologico-Inteligente-Experiencia-do-Paciente.git
cd Fase-5-Cap-1-Assistente-Cardiologico-Inteligente-Experiencia-do-Paciente
```

### 3. Configurar watsonx Assistant
1. Crie uma instância do watsonx Assistant no plano Lite pelo catálogo da IBM Cloud.
2. Em **Global Settings** (engrenagem) → **Upload/Download** → **Upload**, importe o arquivo `watson/Assistente-Cardiológico-Conversacional-action.json`.
3. Abra a Action importada e teste o preview ("dor no peito" e sintomas leves).
4. Obtenha as credenciais em **Environments** → **Draft** → **API details** (URL, Environment ID) e em **Service credentials** (API key).

### 4. Configurar Ambiente Virtual e Instalar Dependências (Global)
O arquivo `requirements.txt` na raiz já reúne todas as dependências do projeto (Backend, Ir Além 1 e Ir Além 2):
```bash
# Criação do venv
python -m venv venv

# Ativação (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativação (Linux / macOS)
source venv/bin/activate

# Instalação de todas as dependências em comando único
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente (`.env`)
Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:
```ini
WATSON_ASSISTANT_API_KEY=sua_api_key_aqui
WATSON_ASSISTANT_URL=https://api.us-south.assistant.watson.cloud.ibm.com/instances/sua_instancia
WATSON_ASSISTANT_ID=seu_assistant_id_aqui
WATSON_ASSISTANT_VERSION=2021-06-14

FLASK_PORT=5000
FLASK_DEBUG=True
```

### 6. Executar o Backend Flask
```bash
cd backend
python run.py
```
O servidor estará acessível em `http://localhost:5000`.

### 7. Executar a Interface do Chatbot (React Native)
```bash
cd frontend
npm install
npx expo start
```
- Para testar no celular físico: escaneie o QR Code com o aplicativo **Expo Go**. Lembre-se de configurar a constante `API_BASE_URL` no arquivo `frontend/app/index.tsx` com o IP local da sua máquina (ex.: `http://192.168.0.15:5000`).
- Para testar no navegador web: pressione a tecla `w` no terminal do Expo.

### 8. Executar o Módulo Ir Além 1 (Extração com CoT e LLM)
```bash
# Certifique-se de que o Ollama está em execução e o modelo baixado
ollama pull llama3.1:8b

# Iniciar o Jupyter Notebook
cd ir_alem_1
jupyter notebook ir_alem_1_extracao_clinica.ipynb
```

### 9. Executar o Módulo Ir Além 2 (Robô de Monitoramento RPA)
```bash
cd ir_alem_2

# 1. Gerar os dados simulados (cria db/clinica.db e mensagens no MongoDB)
python src/gerar_dados_simulados.py

# 2. Executar um ciclo único do robô (demonstração pontual)
python src/robo_monitoramento.py --once

# 3. Ou executar em modo contínuo (automação periódica a cada 60s)
python src/robo_monitoramento.py --intervalo 60
```

---

## Relatórios Técnicos

Todos os relatórios detalhados com metodologia, fundamentação teórica e discussão de resultados estão organizados nos seguintes arquivos:
- **Parte 1 (Assistente & NLP):** [`docs/relatorio_parte1.txt`](docs/relatorio_parte1.txt)
- **Ir Além 1 (IA Generativa & Chain of Thought):** [`ir_alem_1/ir_alem_1.pdf`](ir_alem_1/ir_alem_1.pdf)
- **Ir Além 2 (Automação RPA & Dados Híbridos):** [`ir_alem_2/relatorio_tecnico_ir_alem_2.pdf`](ir_alem_2/relatorio_tecnico_ir_alem_2.pdf)

---

## Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> esta licenciado sob <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

