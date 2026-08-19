# FIAP - Faculdade de Informatica e Administracao Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP" border="0" width="40%" height="40%"></a>
</p>

# 🫀 CardioIA — Assistente Conversacional Cardiológico

O **CardioIA** é um chatbot de saúde digital para triagem e orientação cardiológica inicial. A aplicação usa **IBM Watson Assistant** integrado a um backend em **Python (Flask)** para interpretar mensagens em linguagem natural e responder pacientes com contexto clínico.

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

## Visao Geral



## Estrutura do Projeto

```text
cardio-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # application factory
│   │   ├── routes/
│   │   │   └── chat.py          # endpoints /api/session e /api/message
│   │   └── services/
│   │       └── watson_service.py # encapsula chamadas à API do Watson
│   ├── config.py                # lê variáveis de ambiente (.env)
│   ├── run.py                   # ponto de entrada
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/chat.js
├── watson/
│   └── assistant_export.json    # (você exporta do Watson Assistant depois)
├── docs/
│   └── relatorio.md             # esqueleto do relatório de 1-2 páginas
├── .gitignore
└── README.md
```



## Como Executar



## Licenca

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> esta licenciado sob <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
