from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app import database
from app.auth import linha_autenticada

router = APIRouter(prefix="/linha", tags=["linha"])


@router.get("/consumo")
def consumo(linha: dict = Depends(linha_autenticada)):
    plano = database.PLANOS[linha["plano"]]
    return {
        "plano": linha["plano"],
        "consumo_dados_mb": linha["consumo_dados_mb"],
        "limite_dados_mb": plano["limite_dados_mb"],
        "consumo_minutos": linha["consumo_minutos"],
        "limite_minutos": plano["limite_minutos"],
    }


class TrocarPlanoRequest(BaseModel):
    novo_plano: str


@router.post("/trocar-plano")
def trocar_plano(dados: TrocarPlanoRequest, linha: dict = Depends(linha_autenticada)):
    if dados.novo_plano not in database.PLANOS:
        raise HTTPException(status_code=400, detail="Plano inválido")

    if linha["fatura_em_aberto"]:
        raise HTTPException(status_code=400, detail="Não é possível trocar de plano com fatura em aberto")

    linha["plano"] = dados.novo_plano
    return {"mensagem": "Plano alterado com sucesso", "plano_atual": linha["plano"]}


@router.post("/desativar")
def desativar(linha: dict = Depends(linha_autenticada)):
    if not linha["ativa"]:
        raise HTTPException(status_code=400, detail="Linha já está desativada")

    linha["ativa"] = False
    return {"mensagem": "Linha desativada com sucesso"}


@router.post("/ativar")
def ativar(linha: dict = Depends(linha_autenticada)):
    if linha["ativa"]:
        raise HTTPException(status_code=400, detail="Linha já está ativa")

    linha["ativa"] = True
    return {"mensagem": "Linha ativada com sucesso"}
