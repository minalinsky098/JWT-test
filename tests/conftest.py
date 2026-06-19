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

@pytest.fixture
def new_user_id(client):
    register_payload = {"first_name": "NEW", "last_name":"REGISTER", "email": "newregister@gmail.com","password":"mypassword"}
    res = client.post("/api/v1/register", json = register_payload)
    yield res
    
@pytest.fixture
def setup_header(client, new_user_id):
    data = new_user_id.json()
    header = {"Authorization":f"Bearer {data['token']}"}
    yield header
    client.delete("/api/v1/users", headers=header)
    

    