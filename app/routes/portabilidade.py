from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app import database
from app.auth import linha_autenticada

router = APIRouter(prefix="/portabilidade", tags=["portabilidade"])


class SolicitarPortabilidadeRequest(BaseModel):
    operadora_atual: str


@router.post("/solicitar")
def solicitar(dados: SolicitarPortabilidadeRequest, linha: dict = Depends(linha_autenticada)):
    if not linha["ativa"]:
        raise HTTPException(status_code=400, detail="A linha precisa estar ativa para solicitar portabilidade")

    if linha["fatura_em_aberto"]:
        raise HTTPException(status_code=400, detail="Não é possível portar com fatura em aberto")

    if linha["portabilidade_em_andamento"]:
        raise HTTPException(status_code=400, detail="Já existe uma portabilidade em andamento para esta linha")

    protocolo = database.gerar_protocolo()
    database.portabilidades[protocolo] = {
        "telefone": linha["telefone"],
        "operadora_atual": dados.operadora_atual,
        "status": "em_andamento",
    }
    linha["portabilidade_em_andamento"] = True

    return {"protocolo": protocolo, "status": "em_andamento"}


@router.get("/{protocolo}")
def status(protocolo: str, linha: dict = Depends(linha_autenticada)):
    registro = database.portabilidades.get(protocolo)

    if not registro:
        raise HTTPException(status_code=404, detail="Protocolo não encontrado")

    if registro["telefone"] != linha["telefone"]:
        raise HTTPException(status_code=403, detail="Este protocolo não pertence à sua linha")

    return registro
