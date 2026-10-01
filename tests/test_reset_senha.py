def test_solicitar_reset_para_telefone_existente_gera_codigo(client):
    resposta = client.post("/senha/reset/solicitar", json={"telefone": "11912345678"})

    assert resposta.status_code == 200
    assert "codigo_debug" in resposta.json()
    assert len(resposta.json()["codigo_debug"]) == 6


def test_solicitar_reset_para_telefone_inexistente_nao_revela_a_base(client):
    resposta = client.post("/senha/reset/solicitar", json={"telefone": "11900000000"})

    assert resposta.status_code == 200
    assert "codigo_debug" not in resposta.json()


def test_confirmar_reset_sem_solicitacao_previa_retorna_erro(client):
    resposta = client.post(
        "/senha/reset/confirmar",
        json={"telefone": "11987654321", "codigo": "123456", "nova_senha": "NovaSenha123"},
    )

    assert resposta.status_code == 400
    assert "Nenhuma solicitação" in resposta.json()["detail"]


def test_confirmar_reset_com_codigo_incorreto_retorna_erro(client):
    telefone = "11912345678"
    client.post("/senha/reset/solicitar", json={"telefone": telefone})

    resposta = client.post(
        "/senha/reset/confirmar",
        json={"telefone": telefone, "codigo": "000000", "nova_senha": "NovaSenha123"},
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Código inválido"


def test_confirmar_reset_com_nova_senha_curta_retorna_erro(client):
    telefone = "11912345678"
    solicitar = client.post("/senha/reset/solicitar", json={"telefone": telefone})
    codigo = solicitar.json()["codigo_debug"]

    resposta = client.post(
        "/senha/reset/confirmar",
        json={"telefone": telefone, "codigo": codigo, "nova_senha": "123"},
    )

    assert resposta.status_code == 400


def test_fluxo_completo_de_reset_permite_login_com_nova_senha(client):
    telefone = "11912345678"
    solicitar = client.post("/senha/reset/solicitar", json={"telefone": telefone})
    codigo = solicitar.json()["codigo_debug"]

    confirmar = client.post(
        "/senha/reset/confirmar",
        json={"telefone": telefone, "codigo": codigo, "nova_senha": "SenhaNova@2024"},
    )
    assert confirmar.status_code == 200

    login = client.post("/auth/login", json={"telefone": telefone, "senha": "SenhaNova@2024"})
    assert login.status_code == 200
    assert "token" in login.json()
