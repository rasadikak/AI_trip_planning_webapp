document.addEventListener("DOMContentLoaded", async function() {
    console.log("page loaded");
    const favList = document.getElementById("favList");

    try {
        const response = await fetch("http://127.0.0.1:8000/favDestination/get", {
            method: "GET",
            credentials: "include"
        });
        console.log("response received:", response.status);

        if (!response.ok) throw new Error("Failed to load: " + response.status);

        const data = await response.json();
        console.log("data:", data);

        if (!data || !data.response || data.response.length === 0) {
            favList.innerHTML = "<p>No favourite destinations saved yet.</p>";
            return;
}

        favList.innerHTML = "";

        data.response.forEach(item => {
            console.log("item:", item);
            const div = document.createElement("div");
            div.style.border = "1px solid #ccc";
            div.style.padding = "10px";
            div.style.marginBottom = "10px";

            div.innerHTML = `
                <h3>📍 ${item.destination}</h3>
                <p> Saved on:${new Date(item.created_at).toLocaleDateString()}</p>
                <button onclick="deleteFavourite(${item.id})">🗑️ Remove</button>
            `;

            favList.appendChild(div);
        });

    } catch (error) {
        console.error("Error:", error);
        favList.innerHTML = "<p>Error loading favourites: " + error.message + "</p>";
    }
});

async function deleteFavourite(fav_id) {
    console.log("deleting:", fav_id);
    try {
        const response = await fetch(`http://127.0.0.1:8000/favDestination/${fav_id}`, {
            method: "DELETE",
            credentials: "include"
        });
        console.log("delete response:", response.status);

        if (!response.ok) throw new Error("Failed to delete");

        alert("Removed from favourites!");
        location.reload(); 

    } catch (error) {
        alert("Error: " + error.message);
    }
}