document.getElementById("tripForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    //console.log("1");
    const resultDiv = document.getElementById("tripResult");
    //console.log("2");
    resultDiv.innerHTML = "Creating your Sri Lankan adventure... Please wait. 🐘";
    //console.log("3");

    await new Promise(resolve => setTimeout(resolve, 50));

    try {
        const formData = new FormData(e.target);
        //console.log("4");
        const response = await fetch(`${API_BASE}/planner_api/`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Server responded with an error");
        }

        const result = await response.json();
        //console.log(result);

        resultDiv.innerHTML = marked.parse(result["response"]);
        //console.log("5");

        // Add ⭐ button next to every map link
        const mapLinks = resultDiv.querySelectorAll('a[href*="google.com/maps"]');
    mapLinks.forEach(link => {
    const linkUrl = new URL(link.href);
    let pathParts = linkUrl.pathname.split('/search/');
    let destName = pathParts[1]
        ? decodeURIComponent(pathParts[1])
            .replace(/\+/g, " ")
            .replace(/Sri Lanka/gi, "")
            .trim()
        : link.innerText.trim();

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
        //console.log("Destination:", destination);

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
        //console.log("buttons added");

        // AUTO LOAD ALL MAP LINKS — shows full trip overview on map
        if (typeof loadAllMapLinks === "function") {
            //console.log("Loading all map links...");
            loadAllMapLinks();
        }

    } catch (error) {
        console.error("Error:", error);
        resultDiv.innerHTML = "Error: " + error.message;
        showToast("❌ " + error.message, "error");
    }
});

document.getElementById("tripResult").addEventListener("click", function(e) {
    if (e.target.tagName === 'A' && e.target.href.includes("google.com/maps")) {
        e.preventDefault();
        const url = e.target.href;
        //console.log("Map link clicked:", url);
        window.open(url, '_blank');  // opens in new tab
    }
});

async function saveDestination(destination) {
    try {
        const formData = new FormData();
        formData.append("destination", destination);
        const response = await fetch(`${API_BASE}/favDestination/`, {
            method: "POST",
            body: formData,
            credentials: "include"
        });
        if (response.status==401){
            showToast("⚠️ Session timed out — please log in again","error");
            setTimeout(()=>{
                window.location.href=`${API_BASE}/frontend/home/login.html`;

            }, 2000); //// redirect to login after 2 seconds
            return;
        }
        if (!response.ok) {
            const errData = await response.json();
            showToast(errData.detail, "error");
            return;
        }
        showToast(`⭐ ${destination} saved to favourites!`, "success");
    } catch (error) {
        console.error("Error:", error);
        showToast("Error: " + error.message, "error");
    }
}

async function savePlan(plan, destination) {
    try {
        const formData = new FormData();
        //console.log("save plan 1");
        formData.append("destination", destination);
        //console.log("save plan 2");
        formData.append("plan", plan);
        //console.log("save plan 3");
        const response = await fetch(`${API_BASE}/savedPlans/`, {
            method: "POST",
            body: formData,
            credentials: "include"
        });
        if (response.status==401){
            showToast("⚠️ Session timed out — please log in again","error");
            setTimeout(()=>{
                window.location.href=`${API_BASE}/frontend/home/login.html`;

            }, 2000); //// redirect to login after 2 seconds
            return;
        }
        //console.log("save plan 4");
        if (!response.ok) {
            const errData = await response.json();
            showToast(errData.detail || "Failed to save plan", "error");
            return;
        }
        showToast("💾 Plan saved successfully!", "success");
    } catch (error) {
        console.error("Error:", error);
        showToast("Error saving plan: " + error.message, "error");
    }
}
