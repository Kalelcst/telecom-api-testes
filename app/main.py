from fastapi import FastAPI

from app.routes import linha, login, portabilidade, senha

app = FastAPI(title="Telecom API Teste")

app.include_router(login.router)
app.include_router(senha.router)
app.include_router(linha.router)
app.include_router(portabilidade.router)


@app.get("/")
def raiz():
    return {"mensagem": "API Telecom Teste está no ar"}
