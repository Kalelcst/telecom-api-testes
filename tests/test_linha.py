def _token(client, telefone="11987654321", senha="Senha@123"):
    resposta = client.post("/auth/login", json={"telefone": telefone, "senha": senha})
    return resposta.json()["token"]


def test_consultar_consumo_da_linha(client):
    token = _token(client)

    resposta = client.get("/linha/consumo", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["plano"] == "pos_pago"
    assert corpo["consumo_dados_mb"] == 3000
    assert corpo["limite_dados_mb"] == 15000


def test_trocar_plano_com_sucesso(client):
    token = _token(client)

    resposta = client.post(
        "/linha/trocar-plano", json={"novo_plano": "ilimitado"}, headers={"Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["plano_atual"] == "ilimitado"


def test_trocar_plano_com_fatura_em_aberto_e_bloqueado(client):
    # cliente2 tem fatura_em_aberto = True no seed
    token = _token(client, telefone="11912345678")

    resposta = client.post(
        "/linha/trocar-plano", json={"novo_plano": "ilimitado"}, headers={"Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 400
    assert "fatura em aberto" in resposta.json()["detail"]


def test_trocar_para_plano_invalido_retorna_erro(client):
    token = _token(client)

    resposta = client.post(
        "/linha/trocar-plano", json={"novo_plano": "plano-que-nao-existe"}, headers={"Authorization": f"Bearer {token}"}
    )

    assert resposta.status_code == 400


def test_desativar_linha_ativa_com_sucesso(client):
    token = _token(client)

    resposta = client.post("/linha/desativar", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 200


def test_desativar_linha_ja_desativada_retorna_erro(client):
    token = _token(client)
    client.post("/linha/desativar", headers={"Authorization": f"Bearer {token}"})

    resposta = client.post("/linha/desativar", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 400


def test_ativar_linha_desativada_com_sucesso(client):
    token = _token(client)
    client.post("/linha/desativar", headers={"Authorization": f"Bearer {token}"})

    resposta = client.post("/linha/ativar", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 200
