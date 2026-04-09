import pytest
from backend.main import app
from fastapi.testclient import TestClient






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
    # Register a fresh unverified user
    email = f"unverified_{uuid.uuid4()}@test.com"
    client.post("/register/", data={
        "name": "Unverified User",
        "email": email,
        "password": "Test@1234",
        "confirm_password": "Test@1234"
    }, follow_redirects=False)

    # Now try to login without verifying email
    response = client.post("/login/", data={
        "username": email,
        "password": "Test@1234"
    }, follow_redirects=False)

    print(f"⭐ redirect: {response.headers['location']}")
    assert "not_verified" in response.headers["location"]



