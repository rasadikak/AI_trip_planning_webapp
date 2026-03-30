import pytest
from backend.main import app
from fastapi.testclient import TestClient


client= TestClient(app)

# Register
def test_register_success():
    response = client.post("/register/", data={
        "name": "New User", "email": "new@test.com",
        "password": "Test@1234", "confirm_password": "Test@1234"
    }, follow_redirects=False)
    assert response.status_code == 302
