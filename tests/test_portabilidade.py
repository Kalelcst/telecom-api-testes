def _token(client, telefone="11987654321", senha="Senha@123"):
    resposta = client.post("/auth/login", json={"telefone": telefone, "senha": senha})
    return resposta.json()["token"]


def test_solicitar_portabilidade_com_sucesso(client):
    token = _token(client)

    resposta = client.post(
        "/portabilidade/solicitar", json={"operadora_atual": "OperadoraX"}, headers={"Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "em_andamento"
    assert resposta.json()["protocolo"].startswith("PORT")


def test_solicitar_portabilidade_com_fatura_em_aberto_e_bloqueada(client):
    # cliente2 tem fatura_em_aberto = True no seed
    token = _token(client, telefone="11912345678")

    resposta = client.post(
        "/portabilidade/solicitar", json={"operadora_atual": "OperadoraX"}, headers={"Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 400
    assert "fatura em aberto" in resposta.json()["detail"]


def test_solicitar_portabilidade_ja_em_andamento_retorna_erro(client):
    token = _token(client)
    client.post("/portabilidade/solicitar", json={"operadora_atual": "OperadoraX"}, headers={"Authorization": f"Bearer {token}"})

    resposta = client.post(
        "/portabilidade/solicitar", json={"operadora_atual": "OperadoraX"}, headers={"Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 400
    assert "em andamento" in resposta.json()["detail"]


def test_solicitar_portabilidade_com_linha_inativa_e_bloqueada(client):
    token = _token(client)
    client.post("/linha/desativar", headers={"Authorization": f"Bearer {token}"})

    resposta = client.post(
        "/portabilidade/solicitar", json={"operadora_atual": "OperadoraX"}, headers={"Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 400
    assert "ativa" in resposta.json()["detail"]


def test_consultar_status_de_protocolo_existente(client):
    token = _token(client)
    solicitar = client.post(
        "/portabilidade/solicitar", json={"operadora_atual": "OperadoraX"}, headers={"Authorization": f"Bearer {token}"}
    )
    protocolo = solicitar.json()["protocolo"]

    resposta = client.get(f"/portabilidade/{protocolo}", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "em_andamento"


def test_consultar_protocolo_inexistente_retorna_404(client):
    token = _token(client)

    resposta = client.get("/portabilidade/PORT999999", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 404


def test_consultar_protocolo_de_outra_linha_retorna_403(client):
    token_cliente1 = _token(client)
    solicitar = client.post(
        "/portabilidade/solicitar",
        json={"operadora_atual": "OperadoraX"},
        headers={"Authorization": f"Bearer {token_cliente1}"},
    )
    protocolo = solicitar.json()["protocolo"]

    token_cliente2 = _token(client, telefone="11912345678")
    resposta = client.get(f"/portabilidade/{protocolo}", headers={"Authorization": f"Bearer {token_cliente2}"})

    assert resposta.status_code == 403
