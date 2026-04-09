#Creates a normal test client and a logged-in test client so your tests can call FastAPI endpoints easily

import pytest
from fastapi.testclient import TestClient
from backend.main import app  #So now pytest can test your real API routes.

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c  #This creates a basic test client.

#4️⃣ What about auth_client?=Sometimes you want a client that is already logged in,
#  so you don’t have to log in every time.
@pytest.fixture(scope="module")
def auth_client():
    # Returns a client with a logged-in session cookie
    with TestClient(app) as c: #Creates a test client connected to your FastAPI app.
       # register a test User
       c.post("/register/", data={
           "name": "test user",
           "email":"testUser@gmail.com",
           "password":"admin123@J",
           "confirm_password":"admin123@J"
       })

       #login
       c.post("/login/",data={
           "username":"testUser@gmail.com",
           "password":"admin123@J"
       })
       yield c

       #So this client is now: Logged-in client

#TestClient-It lets you simulate API requests like: client.get("/home/")
#without running the real server.

#scope="module" =This means:
# Create this client once per test file
# Not every test



@pytest.fixture(scope="module")
def auth_client_logged_in():
    with TestClient(app,cookies={}) as c:
        response=c.post("/login/", data={
            "username": "new@test.com",  # ← already exists + already verified in your DB
            "password": "Test@1234"
        }, follow_redirects=False)

        print("\n--- LOGIN DEBUG ---")
        print("Status code:", response.status_code)
        print("Redirect to:", response.headers.get("location"))
        print("Cookies:", c.cookies.jar.__dict__)
        print("-------------------")
        yield c