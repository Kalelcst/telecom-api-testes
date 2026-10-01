import copy

from passlib.hash import bcrypt

# Senha de todas as linhas de seed: "Senha@123"
# (rounds=4 deixa o hash rápido; é só um dado fictício de teste)
_SENHA_HASH = bcrypt.using(rounds=4).hash("Senha@123")

PLANOS = {
    "controle": {"preco": 39.90, "limite_dados_mb": 5000, "limite_minutos": 100},
    "pos_pago": {"preco": 69.90, "limite_dados_mb": 15000, "limite_minutos": 300},
    "ilimitado": {"preco": 99.90, "limite_dados_mb": 50000, "limite_minutos": 1000},
}

# "Banco de dados" em memória (fictício, apenas para testes/portfólio).
_LINHAS_SEED = [
    {
        "id": 1,
        "telefone": "11987654321",
        "cpf": "12345678900",
        "nome": "Cliente Um",
        "senha": _SENHA_HASH,
        "plano": "pos_pago",
        "consumo_dados_mb": 3000,
        "consumo_minutos": 120,
        "ativa": True,
        "fatura_em_aberto": False,
        "portabilidade_em_andamento": False,
    },
    {
        "id": 2,
        "telefone": "11912345678",
        "cpf": "98765432100",
        "nome": "Cliente Dois",
        "senha": _SENHA_HASH,
        "plano": "controle",
        "consumo_dados_mb": 100,
        "consumo_minutos": 10,
        "ativa": True,
        "fatura_em_aberto": True,
        "portabilidade_em_andamento": False,
    },
]

linhas: list = []
codigos_reset: dict = {}
portabilidades: dict = {}
proximo_protocolo = 1


def resetar():
    """Restaura o estado inicial. Usado pelos testes para garantir isolamento."""
    global linhas, codigos_reset, portabilidades, proximo_protocolo
    linhas = copy.deepcopy(_LINHAS_SEED)
    codigos_reset = {}
    portabilidades = {}
    proximo_protocolo = 1


def gerar_protocolo() -> str:
    global proximo_protocolo
    protocolo = f"PORT{proximo_protocolo:06d}"
    proximo_protocolo += 1
    return protocolo


def buscar_por_telefone(telefone: str):
    return next((l for l in linhas if l["telefone"] == telefone), None)


def buscar_por_id(linha_id: int):
    return next((l for l in linhas if l["id"] == linha_id), None)


resetar()
