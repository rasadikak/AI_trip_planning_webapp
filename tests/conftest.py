import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.login.database import SessionLocal
from backend.login import orm_model
from backend.login.utils import hash_password


def create_test_user():
    db = SessionLocal()
    try:
        existing = db.query(orm_model.User).filter_by(email="new@test.com").first()
        if not existing:
            user = orm_model.User(
                name="Test User",
                email="new@test.com",
                password=hash_password("Test@1234"),
                is_verified=True
            )
            db.add(user)
            db.commit()
            print("Test user created")
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    create_test_user()
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def auth_client_logged_in():
    create_test_user()
    with TestClient(app, cookies={}) as c:
        response = c.post("/login/", data={
            "username": "new@test.com",
            "password": "Test@1234"
        }, follow_redirects=False)
        print("\n--- LOGIN DEBUG ---")
        print("Status code:", response.status_code)
        print("Redirect to:", response.headers.get("location"))
        print("-------------------")
        yield c