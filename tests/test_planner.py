import pytest

@pytest.mark.skip(reason="Requires real HuggingFace API token — skipped in CI")
def test_planner_success(auth_client_logged_in):
    response= auth_client_logged_in.post("/planner_api/", data=
                          {"destinationType":"city",
                            "budget":"low",
                            "numDays":1 ,
                            "numPeople":1,
                            "accommodation":"hotel",
                            "foodPreference":["spicy"]})
    assert "response"  in response.json()
    assert response.status_code==200


def test_planner_unsuccess_empty_invalid_days(auth_client_logged_in):
    response= auth_client_logged_in.post("/planner_api/", data=
                          {})
    assert response.status_code==422



def test_planner_unsuccess_invalid_days(auth_client_logged_in):
    response= auth_client_logged_in.post("/planner_api/", data=
                          {"destinationType":"city",
                            "budget":"low",
                            "numDays":0 ,
                            "numPeople":1,
                            "accommodation":"hotel",
                            "foodPreference":["spicy"]})
    assert response.status_code==400

