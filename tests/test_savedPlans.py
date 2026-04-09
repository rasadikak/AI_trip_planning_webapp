import pytest

import uuid


def test_add_savedPlans_auth(auth_client_logged_in):
    response= auth_client_logged_in.post("/savedPlans/", data=
                          {"destination":"mirissa_{uuid.uuid4()}", "plan":"my plan_{uuid.uuid4()}"})
    assert response.status_code==200
    


def test_get_savedPlans_auth(auth_client_logged_in):
    response= auth_client_logged_in.get("/savedPlans/get")
    assert response.status_code==200


def test_delete_favDestinations_auth(auth_client_logged_in):
    response= auth_client_logged_in.delete("/savedPlans/delete/1"
                          )
    assert response.status_code==404

#--------------------------------------------------------




def test_add_savedPlans_no_auth(client):
    response= client.post("/savedPlans/", data=
                          {"destination":"mirissa", "plan":"my plan"})
    assert response.status_code==401
    


def test_get_savedPlans_no_auth(client):
    response= client.get("/savedPlans/get")
    assert response.status_code==401


def test_delete_favDestinations_no_auth(client):
    response= client.delete("/savedPlans/delete/1")
    assert response.status_code==401
