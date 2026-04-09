import pytest
import uuid


# Tests WITH login — should SUCCEED (200)
def test_add_favDestination_success(auth_client_logged_in):
    response = auth_client_logged_in.post("/favDestination/", data={"destination": "mirissa_{uuid.uuid4()}"})
    assert response.status_code == 200

def test_get_favDestination_success(auth_client_logged_in):
    response = auth_client_logged_in.get("/favDestination/get")
    assert response.status_code == 200

def test_delete_favDestination_not_found(auth_client_logged_in):
    response = auth_client_logged_in.delete("/favDestination/delete/99999")  
    assert response.status_code == 404  # logged in but ID doesn't exist

#  Tests WITHOUT login — should get 401
def test_add_favDestination_no_auth(client):   
    response = client.post("/favDestination/", data={"destination": "mirissa"})
    assert response.status_code == 401

def test_get_favDestination_no_auth(client):  
    response = client.get("/favDestination/get")
    assert response.status_code == 401

def test_delete_favDestination_no_auth(client):  
    response = client.delete("/favDestination/delete/1")
    assert response.status_code == 401