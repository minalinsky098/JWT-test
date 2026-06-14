import pytest
from fastapi.testclient import TestClient
from backend.JWTserver import app
from backend.auth import generate_jwt


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def token():
    return generate_jwt("f7bab17f-e834-4ee8-89ca-50638dbfd705")