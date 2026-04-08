import pytest
from conftest import client

def test_add_savedPlans_no_auth(client):
    response= client.post("/savedPlans/", data=
                          {"destination":"mirissa", "plan":"my plan"})
    assert response.status_code==401
    


def test_get_savedPlans_no_auth(client):
    response= client.get("/savedPlans/get")
    assert response.status_code==401


def test_delete_favDestinations_no_auth(client):
    response= client.delete("/savedPlans/delete/1", data=
                          {"plan_id":1})
    assert response.status_code==401




