# Telecom API Testes

![CI](https://github.com/SEU-USUARIO/telecom-api-testes/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![Pytest](https://img.shields.io/badge/tested%20with-Pytest-0A9EDC)

Projeto de portfólio de **automação de testes de API** simulando uma operadora de
telecom fictícia: login por telefone, reset de senha via SMS simulado, consumo de
dados/minutos, troca de plano, ativação/desativação de linha e portabilidade numérica.

> ⚠️ Projeto educacional/fictício. Não representa nenhuma operadora real.

## Cenário simulado

- **Login** por telefone + senha, com token JWT
- **Reset de senha** em duas etapas, simulando envio por SMS
- **Consumo** de dados e minutos frente ao limite do plano contratado
- **Troca de plano**, bloqueada se a linha tiver fatura em aberto
- **Ativação/desativação** de linha
- **Portabilidade numérica**: solicitação com protocolo, bloqueada se a linha estiver
  inativa, com fatura em aberto, ou já tiver uma portabilidade em andamento; consulta
  de status restrita ao dono da linha

| Plano         | Dados   | Minutos |
|---------------|---------|---------|
| controle      | 5 GB    | 100     |
| pos_pago      | 15 GB   | 300     |
| ilimitado     | 50 GB   | 1000    |

Os dados ficam em memória, sem banco real.

## Tecnologias

FastAPI, PyJWT, passlib (bcrypt), Pytest, pytest-cov, GitHub Actions.

## Como rodar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |  Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

pytest                                       # roda a suíte de testes
pytest --cov=app --cov-report=term-missing   # com cobertura
uvicorn app.main:app --reload                # sobe a API (docs em /docs)
```

## Linhas de teste (seed)

| Telefone     | Senha      | Plano     | Fatura em aberto |
|--------------|------------|-----------|-------------------|
| 11987654321  | Senha@123  | pos_pago  | não               |
| 11912345678  | Senha@123  | controle  | sim               |

## Casos de teste cobertos (23)

- **Login** (`test_login.py`): credenciais válidas/inválidas, telefone inexistente, validação automática do Pydantic, rotas protegidas sem token e com token inválido
- **Reset de senha** (`test_reset_senha.py`): geração de código, resposta genérica para telefone inexistente, sem solicitação prévia, código incorreto, senha curta, fluxo completo até o novo login
- **Linha** (`test_linha.py`): consultar consumo, trocar plano, bloqueio por fatura em aberto, plano inválido, ativar/desativar, bloqueio ao desativar linha já desativada
- **Portabilidade** (`test_portabilidade.py`): solicitar com sucesso, bloqueio por fatura em aberto, por portabilidade já em andamento, por linha inativa, consultar status, protocolo inexistente (404) e protocolo de outra linha (403)

> **Isolamento de testes:** a fixture `resetar_banco_de_dados` (em `tests/conftest.py`,
> `autouse=True`) restaura o estado em memória antes de cada teste, então nenhum teste
> depende da ordem de execução.

## Estrutura

```
telecom-api-testes/
├── app/
│   ├── main.py, auth.py, database.py
│   └── routes/ (login, senha, linha, portabilidade)
├── tests/ (conftest.py + 4 arquivos de teste)
├── requirements.txt, pytest.ini
└── .github/workflows/ci.yml
```
