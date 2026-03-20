



document.getElementById("weather_form").addEventListener("submit", async function(e){
    e.preventDefault();
    const resultDiv=document.getElementById("weather-result");
    console.log("weather 1");
    try{
    const place = document.getElementById("weather-input").value.trim();
    print(place)
    if (!place){throw new Error("first input a place")}
    console.log("weather 2");
    const formdata= new FormData(e.target);
    console.log("weather 3");
    formdata.append("place",place);
    const response =await fetch("http://127.0.0.1:8000/weather/",{
        "method":"POST",
        "body": formdata
    });
    console.log("weather 4");

    if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Failed to fetch weather");
    }
    console.log("weather 5");
    const data= await response.json();
    console.log("weather 6");
    
    
    resultDiv.innerHTML = `
            <div style="
                border: 1px solid #ccc;
                border-radius: 12px;
                padding: 20px;
                max-width: 400px;
                background: #f9f9f9;
            ">
                <h3 style="margin:0 0 4px;">
                    📍 ${data.location}, ${data.region}
                </h3>
                <img src="https:${data.icon}" alt="${data.condition}" 
                     style="width:64px; height:64px;">
                <h2 style="margin:0; font-size:2.5rem;">${data.temp_c}°C</h2>
                <p style="margin:0; color:#555;">${data.condition}</p>
                <hr style="margin:12px 0;">
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <div>🌡️ Feels like: <b>${data.feels_like}°C</b></div>
                    <div>💧 Humidity: <b>${data.humidity}%</b></div>
                    <div>💨 Wind: <b>${data.wind_kph} km/h</b></div>
                    <div>👁️ Visibility: <b>${data.visibility} km</b></div>
                    <div>☀️ UV Index: <b>${data.uv_index}</b></div>
                </div>
            </div>
        `;
    }catch(error){
        resultDiv.innerHTML = `<p style="color:red;">❌ ${error.message}</p>`;
        showToast("❌ " + error.message, "error");
    }
});