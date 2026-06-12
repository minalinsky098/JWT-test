import pytest
from fastapi.testclient import TestClient
from backend.JWTserver import app
from backend.auth import generate_jwt


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def token():
    return generate_jwt("f7bab17f-e834-4ee8-89ca-50638dbfd705")