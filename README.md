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

A pasta [`ir_alem_1_extracao_clinica/`](file:///c:/Users/vitor/OneDrive/Documentos/GitHub/Fase-5-Cap-1-Assistente-Cardiologico-Inteligente-Experiencia-do-Paciente/ir_alem_1_extracao_clinica) contém a solução da atividade complementar **Ir Além 1**, que expande o assistente para interpretar e extrair informações de relatos clínicos não estruturados em formato JSON utilizando técnicas avançadas de engenharia de prompt.

### Conteúdo da Pasta

- **[`ir_alem_1_extracao_clinica.ipynb`](file:///c:/Users/vitor/OneDrive/Documentos/GitHub/Fase-5-Cap-1-Assistente-Cardiologico-Inteligente-Experiencia-do-Paciente/ir_alem_1_extracao_clinica/ir_alem_1_extracao_clinica.ipynb):** Jupyter Notebook interativo contendo todo o fluxo de extração, experimentos comparativos e validação de schema.
- **[`ir_alem_1.pdf`](file:///c:/Users/vitor/OneDrive/Documentos/GitHub/Fase-5-Cap-1-Assistente-Cardiologico-Inteligente-Experiencia-do-Paciente/ir_alem_1_extracao_clinica/ir_alem_1.pdf):** Documento com as diretrizes e enunciado da atividade.

### Abordagem Técnica e Destaques

- **Chain of Thought (CoT):** Em vez de solicitar diretamente se o paciente apresenta risco (comportamento "caixa-preta"), o prompt força o modelo a seguir passos explícitos de raciocínio:
  1. Identificação individualizada dos sintomas descritos.
  2. Comparação de cada sintoma com os critérios de alerta cardiológico (*dor no peito, falta de ar, dor no braço, suor frio*).
  3. Classificação final (booleana) acompanhada do resumo narrativo.
- **Validação de Schema com Pydantic:** Integração de validação programática da resposta em JSON com política de retry automático em caso de parsing inválido.
- **Execução via Ollama (`llama3.1:8b`):** Uso de modelo de linguagem local, demonstrando a portabilidade dos conceitos de prompting independentemente da plataforma ou LLM utilizada.
- **Análise Comparativa:** Comparação prática entre a inferência simples (*sem CoT*) e a inferência estruturada com justificativa (*com CoT*), ressaltando os benefícios em termos de transparência e auditabilidade clínica.

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
│   │   └── index.tsx                 # Tela principal da interface do chat
│   ├── app.json                      # Configurações do app Expo
│   └── package.json                  # Dependências do frontend
├── docs/
│   └── relatorio_parte1.txt          # Relatório técnico completo da Parte 1
├── ir_alem_1_extracao_clinica/
│   ├── ir_alem_1.pdf                 # Enunciado da atividade Ir Além 1
│   └── ir_alem_1_extracao_clinica.ipynb # Notebook com extração via CoT e LLM local (Ollama)
├── watson/
│   └── Assistente-Cardiológico-Conversacional-action.json # Exportação oficial da Action do Watson
├── .env.example                      # Modelo das variáveis de ambiente necessárias
├── .gitignore                        # Regras de exclusão de arquivos temporários/segredos
├── requirements.txt                  # Dependências do backend (Flask, ibm-watson, etc.)
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

## Como Executar

### 1. Pré-requisitos
- **Python 3.10+** instalado.
- Instância ativa do **IBM watsonx Assistant** na IBM Cloud com a Action importada (`watson/Assistente-Cardiológico-Conversacional-action.json`).

### 2. Clonar o Repositório
```bash
git clone https://github.com/Vitor985-hub/Fase-5-Cap-1-Assistente-Cardiologico-Inteligente-Experiencia-do-Paciente.git
cd Fase-5-Cap-1-Assistente-Cardiologico-Inteligente-Experiencia-do-Paciente
```
### 3. watsonx Assistant (NLU)
 1. Crie uma instância do watsonx Assistant no plano Lite, pelo catálogo do IBM Cloud.
 2. Dentro do Assistant criado, vá em Global Settings (ícone de engrenagem) → aba Upload/Download → Upload e importe o arquivo .json que está na pasta watson/ deste repositório. Isso recria a action "Relatar sintoma" com todos os steps, condições e variáveis já configurados.
 3. Abra a action importada e clique em Preview para confirmar que o fluxo está funcionando (teste com "estou sentindo dor no peito" e com algo não-crítico, como "sinto cansaço").
 4. Pegue as credenciais necessárias para o backend, na aba Environments → ambiente Draft → API details:
    - Service URL
    - Environment ID (usado como WATSON_ASSISTANT_ID no backend — é o ID do ambiente, não o nome do assistant)
    - API key, em Service credentials, na página da instância no IBM Cloud (fora do builder do Assistant)

### 4. Configurar Ambiente Virtual
```bash
# Criação do venv
python -m venv venv

# Ativação (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativação (Linux / macOS)
source venv/bin/activate
```

### 5. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 6. Configurar Variáveis de Ambiente (`.env`)
Crie um arquivo `.env` na raiz do projeto baseado no `.env.exemple`:
```ini
WATSON_ASSISTANT_API_KEY=sua_api_key_aqui
WATSON_ASSISTANT_URL=https://api.us-south.assistant.watson.cloud.ibm.com/instances/sua_instancia
WATSON_ASSISTANT_ID=seu_assistant_id_aqui
WATSON_ASSISTANT_VERSION=2021-06-14

FLASK_PORT=5000
FLASK_DEBUG=True
```

### 7. Executar o Backend
```bash
cd backend
python run.py
```
O servidor estará acessível em `http://localhost:5000`.

### 8. Executar o App Mobile

```bash
cd frontend
npm install
npx expo start
```
Escaneie o QR code com o app **Expo Go** (Android/iOS). Importante: no arquivo `frontend/app/index.tsx`, a constante `API_BASE_URL` precisa apontar para o IP local do seu computador (ex: `http://192.168.0.10:5000`), não `localhost` — o celular é outro dispositivo na rede.

---

## Relatório Técnico
O relatório técnico detalhado da Parte 1, descrevendo a arquitetura em 3 camadas, modelagem de NLP, lógica de bifurcação de emergência e tratamento de exceções encontra-se disponível em [`docs/relatorio_parte1.txt`](file:///c:/Users/vitor/OneDrive/Documentos/GitHub/Fase-5-Cap-1-Assistente-Cardiologico-Inteligente-Experiencia-do-Paciente/docs/relatorio_parte1.txt).

---

## Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> esta licenciado sob <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

