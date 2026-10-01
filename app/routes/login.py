from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel

from app import database
from app.auth import criar_token

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    telefone: str
    senha: str


@router.post("/login")
def login(dados: LoginRequest):
    linha = database.buscar_por_telefone(dados.telefone)

    if not linha or not bcrypt.verify(dados.senha, linha["senha"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token(linha)
    return {
        "token": token,
        "linha": {"id": linha["id"], "nome": linha["nome"], "telefone": linha["telefone"]},
    }
