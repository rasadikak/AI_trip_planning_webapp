import pytest

from tests.conftest import auth_client








def test_get_profile_success(auth_client_logged_in):
    response= auth_client_logged_in.get("/profile/")
    assert response.status_code==200




def test_editName_auth(auth_client_logged_in):
    response= auth_client_logged_in.patch("/profile/editName", data={"new_name": "New Name"})
    assert response.status_code==200





#---------------------------------------------
#no auth means no cookie
def test_get_profile_unsuccess(client):
    response= client.get("/profile/")
    assert response.status_code==401




def test_editName_no_auth(client):
    response= client.patch("/profile/editName")
    assert response.status_code==401



def test_delete_account_no_auth(client):
    response= client.delete("/profile/delAccount")
    assert response.status_code==401

