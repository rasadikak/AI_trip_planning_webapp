import pytest
from conftest import client

def test_planner_success(client):
    response= client.post("/planner_api/", data=
                          {"destinationType":"city",
                            "budget":"low",
                            "numDays":1 ,
                            "numPeople":1,
                            "accommodation":"hotel",
                            "foodPreference":["spicy"]})
    assert "output"  in response


def test_planner_unsuccess_empty_invalid_days(client):
    response= client.post("/planner_api/", data=
                          {})
    assert response.status_code==422


#Basic prompt injection detection test
def test_chatbot_unsuccess_two(client):
    response= client.post("/planner_api/", data=
                          {"destinationType":"city",
                            "budget":"low",
                            "numDays":0 ,
                            "numPeople":1,
                            "accommodation":"hotel",
                            "foodPreference":["spicy"]})
    assert response.status_code==400

