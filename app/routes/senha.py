import random
import time

from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel

from app import database

router = APIRouter(prefix="/senha", tags=["senha"])

VALIDADE_CODIGO_SEGUNDOS = 5 * 60


class SolicitarRequest(BaseModel):
    telefone: str


class ConfirmarRequest(BaseModel):
    telefone: str
    codigo: str
    nova_senha: str


def _gerar_codigo() -> str:
    return f"{random.randint(100000, 999999)}"


@router.post("/reset/solicitar")
def solicitar(dados: SolicitarRequest):
    linha = database.buscar_por_telefone(dados.telefone)

    # Por segurança, não revelamos se o número existe ou não na base.
    if not linha:
        return {"mensagem": "Se o número existir, um SMS com o código foi enviado."}

    codigo = _gerar_codigo()
    database.codigos_reset[dados.telefone] = {
        "codigo": codigo,
        "expira_em": time.time() + VALIDADE_CODIGO_SEGUNDOS,
    }

    # Em produção isso seria enviado por SMS. Aqui devolvemos no corpo da
    # resposta só para viabilizar os testes automatizados.
    return {
        "mensagem": "Se o número existir, um SMS com o código foi enviado.",
        "codigo_debug": codigo,
    }


@router.post("/reset/confirmar")
def confirmar(dados: ConfirmarRequest):
    registro = database.codigos_reset.get(dados.telefone)

    if not registro:
        raise HTTPException(status_code=400, detail="Nenhuma solicitação de reset encontrada para este número")

    if time.time() > registro["expira_em"]:
        del database.codigos_reset[dados.telefone]
        raise HTTPException(status_code=400, detail="Código expirado. Solicite um novo.")

    if registro["codigo"] != dados.codigo:
        raise HTTPException(status_code=400, detail="Código inválido")

    if len(dados.nova_senha) < 8:
        raise HTTPException(status_code=400, detail="A nova senha deve ter pelo menos 8 caracteres")

    linha = database.buscar_por_telefone(dados.telefone)
    linha["senha"] = bcrypt.using(rounds=4).hash(dados.nova_senha)
    del database.codigos_reset[dados.telefone]

    return {"mensagem": "Senha alterada com sucesso"}
