import pytest
from backend.main import app
from fastapi.testclient import TestClient
from tests.conftest import client, auth_client





import uuid



def test_register_success(client):

    email = f"user_{uuid.uuid4()}@test.com"

    response = client.post(
        "/register/",
        data={
            "name": "New User",
            "email": email,
            "password": "Test@1234",
            "confirm_password": "Test@1234"
        }, follow_redirects=False
    )
    print(f" ⭐code for test_register_success ",response.status_code)

    assert response.status_code == 302
    

   


def test_login_success(client):
    response = client.post("/login/", data={
         "username": "new@test.com",
        "password": "Test@1234"
    }, follow_redirects=False)
    print(f" ⭐code for test_login_success ",response.status_code)
    assert response.status_code == 302


def test_login_wrong_pw(client):
    response= client.post("/login/", data={
        "username":"new@test.com",
        "password":"wrong_pw"
    }, follow_redirects=False
    )
    print(f" ⭐code for test_login_wrong_pw ",response.status_code)
    assert response.status_code==302


def test_login_wrong_username(client):
    response= client.post("/login/", data={
        "username":"wrong@test.com",
        "password":"Test@1234"
    }, follow_redirects=False
    )
    print(f" ⭐code for test_login_wrong_username ",response.status_code)
    assert response.status_code==302


def test_login_wrong_username_and_pw(client):
    response= client.post("/login/", data={
        "username":"wrong@test.com",
        "password":"wrong@1234"
    }, follow_redirects=False
    )
    print(f" ⭐code for test_login_wrong_username_and_pw ",response.status_code)
    assert response.status_code==302


def test_login_not_verified(client):
    response = client.post("/login/", data={
        "username": "unverified@test.com", "password": "Test@1234"
    }, follow_redirects=False)
    assert "not_verified" in response.headers["location"]

# -------------weather tests-----------

def test_weather_success(client):
    response= client.post("/weather", data={
        "place":"colombo"
    })
    print(f" ⭐code for test_weather_success ",response.status_code)
    assert response.status_code==200



def test_weather_empty_place(client):
    response = client.post("/weather/", data={"place": ""})
    assert response.status_code == 422  # FastAPI validation error

