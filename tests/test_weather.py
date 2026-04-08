from tests.conftest import client

# -------------weather tests-----------

def test_weather_success(client):
    response= client.post("/weather", data={
        "place":"colombo"
    })
    print(f" ⭐code for test_weather_success ",response.status_code)
    assert response.status_code==200



def test_weather_empty_place(client):
    response = client.post("/weather/", data={"place": ""})
    assert response.status_code == 422  # FastAPI validation error