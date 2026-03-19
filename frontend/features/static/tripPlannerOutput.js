document.getElementById("tripForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    console.log("1");
    const resultDiv = document.getElementById("tripResult");
    console.log("2");
    resultDiv.innerHTML = "Creating your Sri Lankan adventure... Please wait. 🐘"; // Loading state
    console.log("3");

     // allow browser to repaint
    await new Promise(resolve => setTimeout(resolve, 50));
    
    try {
        const formData = new FormData(e.target);
        console.log("4");
        const response = await fetch("http://127.0.0.1:8000/planner_api/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Server responded with an error");

        const result = await response.json();
        console.log(result)
        // result["trip plan"] matches your Python return key
        resultDiv.innerHTML = marked.parse(result["response"]);
        console.log("5")
    } catch (error) {
        resultDiv.innerHTML = "Error: " + error.message;
    }
});

document.getElementById("tripResult").addEventListener("click", function(e){
    if (e.target.tagName== 'A' && e.target.href.includes("dest_name")){
        e.preventDefault();
        const url= new URL(e.target.href);
        const dest_name= url.searchParams.get("dest_name");
        console.log(dest_name);
        if (typeof fetchLocation=="function"){
            fetchLocation(dest_name);

        }else{
            console.error("fetchLocation function not found! Make sure map.js is loaded.");
        }
    }
});



document.getElementById("tripResult").addEventListener("DOMContentLoaded", async function(e){
    e.preventDefault();

    // Extract destination from response (first heading or first line)
    const firstLine = result["response"].split('\n').find(line => line.trim() !== '');
    const destination = firstLine.replace(/[#*]/g, '').trim();
    console.log(destination);

    const buttonDiv= document.createElement("div");
    buttonDiv.style.marginTop = "20px";
    buttonDiv.style.display = "flex";
    buttonDiv.style.gap = "10px";

    const favouriteButton= document.createElement("button");
    favouriteButton.innerText="⭐ Save Destination";
    favouriteButton.onclick = () => {saveDestination(destination)}

    const savePlanButton= document.createElement("button");
    favouriteButton.innerText="💾 Save Plan";

    resultDiv.appendChild(buttonDiv);
    buttonDiv.appendChild(favouriteButton);
    buttonDiv.appendChild(savePlanButton);
});



function saveDestination(dest_name){
    pass
}