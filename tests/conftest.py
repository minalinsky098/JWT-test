import pytest
from fastapi.testclient import TestClient
from backend.JWTserver import app
from backend.auth import generate_jwt
import os
os.environ["DEV_MODE"] = "false"

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def token():
    return generate_jwt("498592a0-5408-487d-aa0d-1cd6be2d0853")