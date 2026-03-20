document.addEventListener("DOMContentLoaded", async function() {
    //console.log("page loaded");
    const favList = document.getElementById("favList");
    try {
        const response = await fetch(`${API_BASE}/favDestination/get`, {
            method: "GET",
            credentials: "include"
        });
        //console.log("response received:", response.status);
        if (response.status==401){
            showToast("⚠️ Session timed out — please log in again","error");
            setTimeout(()=>{
                window.location.href=`${API_BASE}/frontend/home/login.html`;

            }, 2000); //// redirect to login after 2 seconds
            return;
        }
        if (!response.ok) throw new Error("Failed to load: " + response.status);
        const data = await response.json();
        //console.log("data:", data);
        if (!data || !data.response || data.response.length === 0) {
            favList.innerHTML = "<p>No favourite destinations saved yet.</p>";
            return;
}
        favList.innerHTML = "";
        data.response.forEach(item => {
            //console.log("item:", item);
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
        //console.error("Error:", error);
        favList.innerHTML = "<p>Error loading favourites: " + error.message + "</p>";
    }
});
async function deleteFavourite(fav_id) {
    //console.log("deleting:", fav_id);
    try {
        const response = await fetch(`${API_BASE}/favDestination/delete/${fav_id}`, {
            method: "DELETE",
            credentials: "include"
        });

        if (response.status==401){
            showToast("⚠️ Session timed out — please log in again","error");
            setTimeout(()=>{
                window.location.href=`${API_BASE}/frontend/home/login.html`;

            }, 2000); //// redirect to login after 2 seconds
            return;
        }
        //console.log("delete response:", response.status);
        if (!response.ok) throw new Error("Failed to delete");
        showToast("🗑️ Removed from favourites", "warning");
        location.reload(); 
    } catch (error) {
        showToast("Error: " + error.message, "error");
    }
}