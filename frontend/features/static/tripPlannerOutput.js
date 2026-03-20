document.getElementById("tripForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    console.log("1");
    const resultDiv = document.getElementById("tripResult");
    console.log("2");
    resultDiv.innerHTML = "Creating your Sri Lankan adventure... Please wait. 🐘";
    console.log("3");

    await new Promise(resolve => setTimeout(resolve, 50));

    try {
        const formData = new FormData(e.target);
        console.log("4");
        const response = await fetch("http://127.0.0.1:8000/planner_api/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Server responded with an error");
        }

        const result = await response.json();
        console.log(result);

        resultDiv.innerHTML = marked.parse(result["response"]);
        console.log("5");

        // Add ⭐ button next to every map link
        const mapLinks = resultDiv.querySelectorAll('a[href*="dest_name"]');
        mapLinks.forEach(link => {
            const linkUrl = new URL(link.href);
            let destName = linkUrl.searchParams.get("dest_name");
            destName = destName.replace(/\+/g, " ").replace(/_/g, " ").trim();

            const starBtn = document.createElement("button");
            starBtn.innerText = "⭐";
            starBtn.title = `Save ${destName} to favourites`;
            starBtn.style.marginLeft = "6px";
            starBtn.style.padding = "2px 8px";
            starBtn.style.cursor = "pointer";
            starBtn.style.fontSize = "0.85rem";
            starBtn.style.border = "1px solid #ccc";
            starBtn.style.borderRadius = "4px";
            starBtn.style.background = "#fffde7";
            starBtn.onclick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                saveDestination(destName);
            };
            link.insertAdjacentElement("afterend", starBtn);
        });

        // Extract first destination for Save Plan button
        const mapLinkMatch = result["response"].match(/dest_name=([^)\s\n&]+)/);
        let destination = "";
        if (mapLinkMatch) {
            destination = decodeURIComponent(mapLinkMatch[1])
                .replace(/\+/g, " ")
                .replace(/_/g, " ")
                .trim();
        } else {
            const destType = document.getElementById("destinationType").value;
            destination = destType.charAt(0).toUpperCase() + destType.slice(1);
        }
        console.log("Destination:", destination);

        // Save Plan button at bottom
        const buttonDiv = document.createElement("div");
        buttonDiv.style.marginTop = "20px";
        buttonDiv.style.display = "flex";
        buttonDiv.style.gap = "10px";

        const savePlanButton = document.createElement("button");
        savePlanButton.innerText = "💾 Save Plan";
        savePlanButton.onclick = () => savePlan(result["response"], destination);

        buttonDiv.appendChild(savePlanButton);
        resultDiv.appendChild(buttonDiv);
        console.log("buttons added");

        // AUTO LOAD ALL MAP LINKS — shows full trip overview on map
        if (typeof loadAllMapLinks === "function") {
            console.log("Loading all map links...");
            loadAllMapLinks();
        }

    } catch (error) {
        resultDiv.innerHTML = "Error: " + error.message;
        showToast("❌ " + error.message, "error");
    }
});

// ── Map link click — highlight marker instead of reloading map ──────
document.getElementById("tripResult").addEventListener("click", function(e) {
    if (e.target.tagName === 'A' && e.target.href.includes("dest_name")) {
        e.preventDefault();
        const url = new URL(e.target.href);
        let dest_name = url.searchParams.get("dest_name");
        dest_name = dest_name.replace(/\+/g, " ").replace(/_/g, " ").trim();
        console.log("Map link clicked:", dest_name);
        console.log("Current markers:", Object.keys(markers));        // ADD
        console.log("highlightMarker exists:", typeof highlightMarker); // ADD
        console.log("map object:", map);                      

        if (typeof highlightMarker === "function") {
            highlightMarker(dest_name);
        } else {
            console.error("highlightMarker not found — is map.js loaded?");
        }
    }
});

async function saveDestination(destination) {
    try {
        const formData = new FormData();
        formData.append("destination", destination);
        const response = await fetch("http://127.0.0.1:8000/favDestination/", {
            method: "POST",
            body: formData,
            credentials: "include"
        });
        if (!response.ok) {
            const errData = await response.json();
            showToast(errData.detail, "error");
            return;
        }
        showToast(`⭐ ${destination} saved to favourites!`, "success");
    } catch (error) {
        showToast("Error: " + error.message, "error");
    }
}

async function savePlan(plan, destination) {
    try {
        const formData = new FormData();
        console.log("save plan 1");
        formData.append("destination", destination);
        console.log("save plan 2");
        formData.append("plan", plan);
        console.log("save plan 3");
        const response = await fetch("http://127.0.0.1:8000/savedPlans/", {
            method: "POST",
            body: formData,
            credentials: "include"
        });
        console.log("save plan 4");
        if (!response.ok) {
            const errData = await response.json();
            showToast(errData.detail || "Failed to save plan", "error");
            return;
        }
        showToast("💾 Plan saved successfully!", "success");
    } catch (error) {
        showToast("Error saving plan: " + error.message, "error");
    }
}
