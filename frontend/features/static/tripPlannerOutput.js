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

    } catch (error) {
        resultDiv.innerHTML = "Error: " + error.message;
    }
});





document.getElementById("tripResult").addEventListener("click", function(e) {
    if (e.target.tagName === 'A' && e.target.href.includes("dest_name")) {
        e.preventDefault();
        const url = new URL(e.target.href);
        let dest_name = url.searchParams.get("dest_name");
        dest_name = dest_name.replace(/\+/g, " ").replace(/_/g, " ").trim();
        console.log("Map clicked:", dest_name);

        if (typeof fetchLocation === "function") {
            fetchLocation(dest_name).then(() => {
                // Scroll AFTER map is fully loaded
                setTimeout(() => {
                    document.getElementById("map-section").scrollIntoView({ 
                        behavior: "smooth",
                        block: "start"
                    });
                }, 400);
            });
        } else {
            console.error("fetchLocation not found");
        }
    }
});







async function saveDestination(destination){
    try{
        const formData= new FormData();
        console.log("save dest 1");
        formData.append("destination", destination);
        console.log("save dest 2");
        const response= await fetch("http://127.0.0.1:8000/favDestination/",{
            method:"POST",
            body:formData,
            credentials:"include"
        });
        console.log("save dest 3");

        if(!response.ok){
            throw new Error("Error:", Error);
        }else{
            alert("Destination saved to favourites!")
            console.log("save dest 4");
        }
    }catch(error){
        alert("Error saving destination: " + error.message);
    }
    
}


async function savePlan(plan, destination){
    try{
        const formData= new FormData();
        console.log("save plan 1");
        formData.append("destination", destination);
        console.log("save plan 2");
        formData.append("plan", plan);
        console.log("save plan 3");
        const response= await fetch("http://127.0.0.1:8000/savedPlans/",{
            method:"POST",
            body:formData,
            credentials:"include"
        });
        console.log("save plan 4");

        if(!response.ok){
            throw new Error("Error:", Error);
        }else{
            alert("plan is saved!")
        }
    }catch(error){
        alert("Error saving plan: " + error.message);
    }
}