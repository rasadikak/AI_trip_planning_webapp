let map;
let marker;


async function fetchLocation(destName) {
    const response = await fetch(`http://127.0.0.1:8000/map/json/?dest_name=${encodeURIComponent(destName)}`);
    const data = await response.json();
    const lat = parseFloat(data.lat);
    const lon = parseFloat(data.lng);
    
    // Hide placeholder, show map
    document.getElementById("map-placeholder").style.display = "none";
    
    showMap(lat, lon, data.name);
}

function showMap(lat, lng, placeName) {

    // Show map section
    document.getElementById("map-section").style.display = "block";
    document.getElementById("map-title").innerText = placeName;

    // If map not initialized, create it
    if (!map) {
        map = L.map('map').setView([lat, lng], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap'
        }).addTo(map);
    } else {
        map.setView([lat, lng], 13);
    }

    // Remove previous marker if exists
    if (marker) {
        map.removeLayer(marker);
    }

    // Add new marker
    marker = L.marker([lat, lng]).addTo(map)
        .bindPopup(placeName)
        .openPopup();
}