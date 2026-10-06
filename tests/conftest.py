import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture(autouse=True)
def resetar_banco_de_dados():
    database.resetar()
    yield


@pytest.fixture
def client():
    return TestClient(app)
