def test_login_com_credenciais_validas_retorna_token(client):
    resposta = client.post("/auth/login", json={"telefone": "11987654321", "senha": "Senha@123"})

    assert resposta.status_code == 200
    assert "token" in resposta.json()
    assert resposta.json()["linha"]["telefone"] == "11987654321"


def test_login_com_senha_incorreta_retorna_401(client):
    resposta = client.post("/auth/login", json={"telefone": "11987654321", "senha": "senhaErrada"})

    assert resposta.status_code == 401


def test_login_com_telefone_nao_cadastrado_retorna_401(client):
    resposta = client.post("/auth/login", json={"telefone": "11900000000", "senha": "Senha@123"})

    assert resposta.status_code == 401


def test_login_sem_senha_retorna_erro_de_validacao(client):
    resposta = client.post("/auth/login", json={"telefone": "11987654321"})

    assert resposta.status_code == 422


def test_rota_protegida_bloqueia_acesso_sem_token(client):
    resposta = client.get("/linha/consumo")

    assert resposta.status_code == 401


def test_rota_protegida_bloqueia_acesso_com_token_invalido(client):
    resposta = client.get("/linha/consumo", headers={"Authorization": "Bearer token-invalido"})

    assert resposta.status_code == 401


def test_rota_protegida_permite_acesso_com_token_valido(client):
    login_resposta = client.post("/auth/login", json={"telefone": "11987654321", "senha": "Senha@123"})
    token = login_resposta.json()["token"]

    resposta = client.get("/linha/consumo", headers={"Authorization": f"Bearer {token}"})

    assert resposta.status_code == 200
