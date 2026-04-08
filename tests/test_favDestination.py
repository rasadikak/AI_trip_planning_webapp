import pytest
from conftest import client

def test_add_favDestinations_no_auth(client):
    response= client.post("/favDestination/", data=
                          {"destination":"mirissa"})
    assert response.status_code==401
    


def test_get_favDestinations_no_auth(client):
    response= client.get("/favDestination/get")
    assert response.status_code==401


def test_delete_favDestinations_no_auth(client):
    response= client.delete("/favDestination/delete/1", data=
                          {"fav_id":1})
    assert response.status_code==401




