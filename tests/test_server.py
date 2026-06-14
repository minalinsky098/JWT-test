import pytest
from fastapi.testclient import TestClient

async def test_get_all_users(client):
    res = client.get("/api/v1/users")
    assert res.status_code == 200

async def test_login_wrong_email(client):
    payload = {"email": "thisismyemail", "password": "mypassword"}
    res = client.post("/api/v1/login",json = payload)
    assert res.status_code == 422
    
async def test_login_empty_payload(client):
    payload = {}
    res = client.post("/api/v1/login",json = payload)
    assert res.status_code == 422
    
async def test_login_empty_email(client):
    payload = {"email": "","password":"mypassword"}
    res = client.post("/api/v1/login",json = payload)
    assert res.status_code == 422
    
async def test_login_not_registered(client):
    payload = {"email": "email@gmail.com","password":"mypassword"}
    res = client.post("/api/v1/login", json = payload)
    data = res.json()
    assert res.status_code == 401
    assert data["detail"] == "User is not registered"
    
async def test_login_wrong_password(client):
    payload = {"email": "alboloter@gmail.com","password":"Mypassword"}
    res = client.post("/api/v1/login", json = payload)
    data = res.json()
    assert res.status_code == 401   
    assert data["detail"] == "Invalid password"
    
async def test_login_happy(client):
    payload = {"email": "alboloter@gmail.com","password":"mypassword"}
    res = client.post("/api/v1/login", json = payload)
    data = res.json()
    assert res.status_code == 200
    assert "token" in data
    assert data["token"] is not None
    assert data["token"] != ""
    assert data["detail"] == "User logged in"    
    