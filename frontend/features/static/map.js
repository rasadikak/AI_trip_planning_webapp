let map;
let markers = {};
let routeLine = null;
let allLocations = [];

// ── Custom numbered marker ──────────────────────────────────────────
function createNumberedIcon(number) {
    return L.divIcon({
        html: `
            <div style="
                background: linear-gradient(135deg, #1B5E20, #2E7D32);
                width: 36px;
                height: 36px;
                border-radius: 50% 50% 50% 0;
                transform: rotate(-45deg);
                border: 3px solid white;
                box-shadow: 0 3px 10px rgba(0,0,0,0.4);
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <span style="
                    transform: rotate(45deg);
                    color: white;
                    font-size: 0.8rem;
                    font-weight: 700;
                    font-family: sans-serif;
                ">${number}</span>
            </div>`,
        iconSize: [36, 36],
        iconAnchor: [18, 36],
        popupAnchor: [0, -36],
        className: ''
    });
}

// ── Initialize map ──────────────────────────────────────────────────
function initMap() {
    if (map) return;

    map = L.map('map', {
        zoomControl: true,
        scrollWheelZoom: true
    }).setView([7.8731, 80.7718], 8); // center of Sri Lanka

    // CartoDB Voyager — colorful, clear, modern
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> © <a href="https://carto.com/">CartoDB</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Scale bar
    L.control.scale({
        imperial: false,
        position: 'bottomright'
    }).addTo(map);
}

// ── Build popup HTML ────────────────────────────────────────────────
function buildPopup(data, number) {
    const name     = data.name     || '';
    const city     = data.city     || '';
    const district = data.district || '';
    const province = data.province || '';
    const type     = data.type     || '';

    return `
        <div style="min-width:180px; font-family:'Segoe UI',sans-serif;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <div style="
                    background:#2E7D32;
                    color:white;
                    width:22px; height:22px;
                    border-radius:50%;
                    display:flex; align-items:center; justify-content:center;
                    font-size:0.75rem; font-weight:700;
                    flex-shrink:0;
                ">${number}</div>
                <h3 style="margin:0; color:#2E7D32; font-size:1rem;">${name}</h3>
            </div>
            ${city     ? `<p style="margin:0;      font-size:0.83rem;">📍 ${city}</p>`     : ''}
            ${district ? `<p style="margin:2px 0;  font-size:0.83rem;">🗺️ ${district}</p>` : ''}
            ${province ? `<p style="margin:2px 0;  font-size:0.83rem;">🇱🇰 ${province}</p>` : ''}
            ${type     ? `<p style="margin:6px 0 0;font-size:0.78rem; color:#666;">📌 ${type}</p>` : ''}
        </div>
    `;
}

// ── Draw dashed route line between all markers ──────────────────────
function drawRouteLine(locations) {
    if (routeLine) {
        map.removeLayer(routeLine);
        routeLine = null;
    }

    if (locations.length < 2) return;

    const latlngs = locations.map(loc => [
        parseFloat(loc.lat),
        parseFloat(loc.lng)
    ]);

    routeLine = L.polyline(latlngs, {
        color     : '#F9A825',  // gold — matches Serendib theme
        weight    : 3,
        opacity   : 0.8,
        dashArray : '8, 8',
        lineJoin  : 'round'
    }).addTo(map);
}

// ── Show all locations on map at once ───────────────────────────────
function showAllOnMap(locations) {
    if (!locations || locations.length === 0) return;

    initMap();

    document.getElementById("map-section").style.display  = "block";
    document.getElementById("map-placeholder").style.display = "none";
    document.getElementById("map-title").innerText =
        `🗺️ Trip Map — ${locations.length} destination${locations.length > 1 ? 's' : ''}`;

    // Clear existing markers
    Object.values(markers).forEach(m => map.removeLayer(m));
    markers      = {};
    allLocations = locations;

    const bounds = [];

    locations.forEach((data, index) => {
        const lat    = parseFloat(data.lat);
        const lng    = parseFloat(data.lng);
        const number = index + 1;

        const m = L.marker([lat, lng], { icon: createNumberedIcon(number) })
            .addTo(map)
            .bindPopup(buildPopup(data, number));

        markers[data.name.toLowerCase()] = m;
        bounds.push([lat, lng]);
    });

    // Draw dashed gold route line
    drawRouteLine(locations);

    // Auto fit map to show all markers
    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] });
    }

    setTimeout(() => map.invalidateSize(), 200);
}

// ── Highlight a specific marker when user clicks a link ─────────────
function highlightMarker(destName) {
    const key = destName.toLowerCase();
    const m   = markers[key];

    if (m) {
        // Pan smoothly to marker and open popup
        map.flyTo(m.getLatLng(), 13, { duration: 1.2 });
        setTimeout(() => m.openPopup(), 1200);
        document.getElementById("map-title").innerText = `📍 ${destName}`;

        // Scroll to map section
        setTimeout(() => {
            document.getElementById("map-section").scrollIntoView({
                behavior: "smooth",
                block   : "start"
            });
        }, 300);

    } else {
        // Marker not loaded yet — fetch and add it
        fetchAndAddMarker(destName);
    }
}

// ── Fetch a single location and add to existing map ─────────────────
async function fetchAndAddMarker(destName) {
    try {
        const response = await fetch(
            `http://127.0.0.1:8000/map/json/?dest_name=${encodeURIComponent(destName)}`
        );

        if (!response.ok) {
            console.error("Location not found:", destName);
            return;
        }

        const data   = await response.json();
        const lat    = parseFloat(data.lat);
        const lng    = parseFloat(data.lng);
        const number = Object.keys(markers).length + 1;

        initMap();
        document.getElementById("map-section").style.display     = "block";
        document.getElementById("map-placeholder").style.display = "none";

        // CartoDB Voyager tile (in case map was not yet initialized)
        const m = L.marker([lat, lng], { icon: createNumberedIcon(number) })
            .addTo(map)
            .bindPopup(buildPopup(data, number))
            .openPopup();

        markers[data.name.toLowerCase()] = m;
        allLocations.push(data);

        map.flyTo([lat, lng], 13, { duration: 1.2 });
        document.getElementById("map-title").innerText = `📍 ${destName}`;

        // Scroll to map
        setTimeout(() => {
            document.getElementById("map-section").scrollIntoView({
                behavior: "smooth",
                block   : "start"
            });
        }, 300);

        setTimeout(() => map.invalidateSize(), 200);

    } catch (error) {
        console.error("Map fetch error:", error);
    }
}

// ── Load ALL map links from trip result at once ─────────────────────
async function loadAllMapLinks() {
    const tripResult = document.getElementById("tripResult");
    if (!tripResult) return;

    const links = tripResult.querySelectorAll('a[href*="dest_name"]');
    if (links.length === 0) {
        console.log("No map links found in plan");
        return;
    }

    // Deduplicate destination names
    const seen     = new Set();
    const unique   = [];
    links.forEach(link => {
        const url      = new URL(link.href);
        let destName   = url.searchParams.get("dest_name");
        destName       = destName.replace(/\+/g, " ").replace(/_/g, " ").trim().toLowerCase();
        if (!seen.has(destName)) {
            seen.add(destName);
            unique.push({ link, destName });
        }
    });

    console.log(`Found ${unique.length} unique map links — loading all...`);

    const fetchPromises = unique.map(async ({ destName }) => {
        try {
            const response = await fetch(
                `http://127.0.0.1:8000/map/json/?dest_name=${encodeURIComponent(destName)}`
            );
            if (response.ok) {
                const data = await response.json();
                console.log("Loaded:", destName);
                return data;
            }
        } catch (error) {
            console.error("Failed to load:", destName, error);
        }
        return null;
    });

    // Fetch all in parallel
    const results        = await Promise.all(fetchPromises);
    const validLocations = results.filter(r => r !== null);

    console.log(`Successfully loaded ${validLocations.length} locations`);

    if (validLocations.length > 0) {
        showAllOnMap(validLocations);
    }
}

// ── Legacy fetchLocation — kept for compatibility ───────────────────
async function fetchLocation(destName) {
    highlightMarker(destName);
}