import os
import time

import jwt
from fastapi import Header, HTTPException

from app import database

SEGREDO_JWT = os.environ.get("JWT_SECRET", "segredo-de-teste-nao-usar-em-producao")
ALGORITMO = "HS256"
VALIDADE_SEGUNDOS = 3600


def criar_token(linha: dict) -> str:
    payload = {"sub": linha["telefone"], "exp": int(time.time()) + VALIDADE_SEGUNDOS}
    return jwt.encode(payload, SEGREDO_JWT, algorithm=ALGORITMO)


def linha_autenticada(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token não fornecido")

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SEGREDO_JWT, algorithms=[ALGORITMO])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    linha = database.buscar_por_telefone(payload["sub"])
    if not linha:
        raise HTTPException(status_code=401, detail="Linha não encontrada")

    return linha
