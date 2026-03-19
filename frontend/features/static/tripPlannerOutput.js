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
        console.log("5");

        const firstLine = result["response"].split('\n').find(line => line.trim() !== '');
        const destination = firstLine.replace(/[#*]/g, '').trim();
        console.log("Destination:", destination);

        
        const buttonDiv = document.createElement("div");
        buttonDiv.style.marginTop = "20px";
        buttonDiv.style.display = "flex";
        buttonDiv.style.gap = "10px";
        console.log("buttons creted");

        const favouriteButton = document.createElement("button");
        favouriteButton.innerText = "⭐ Save Destination";
        console.log("fav buttons creted");
        favouriteButton.onclick = () => saveDestination(destination);
        console.log("fav buttons creted 2");


        const savePlanButton = document.createElement("button");
        savePlanButton.innerText = "💾 Save Plan";   
        console.log("save plan buttons creted");
        savePlanButton.onclick = () => savePlan(result["response"], destination);
        console.log("save plan buttons creted 2");

        buttonDiv.appendChild(favouriteButton);
        console.log("button appended 1");
        buttonDiv.appendChild(savePlanButton);
        console.log("button appended 2");
        resultDiv.appendChild(buttonDiv);
        console.log("button appended 3");

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