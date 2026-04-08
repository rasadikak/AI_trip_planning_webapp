import pytest
from conftest import client


#no auth mens no cookie
def test_get_profile_unsuccess(client):
    response= client.get("/profile/")
    assert response.status_code==401




def test_editName_no_auth(client):
    response= client.patch("/profile/editName")
    assert response.status_code==401



def test_delete_account_no_auth(client):
    response= client.delete("/profile/delAccount")
    assert response.status_code==401

