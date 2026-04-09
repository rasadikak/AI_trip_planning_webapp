

# -------------weather tests-----------

def test_weather_success(auth_client_logged_in):
    response= auth_client_logged_in.post("/weather/", data={
        "place":"colombo"
    })
    print(f" ⭐code for test_weather_success ",response.status_code)
    assert response.status_code==200
    data= response.json()
    assert "temp_c" in data
    assert "feels_like" in data
    assert "condition" in data
    assert "humidity" in data
    assert "wind_kph" in data
    assert "visibility" in data
    assert "uv_index" in data



def test_weather_empty_place(auth_client_logged_in):
    response = auth_client_logged_in.post("/weather/", data={"place": ""})
    assert response.status_code == 422  # FastAPI validation error