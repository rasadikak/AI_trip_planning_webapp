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



function attachMapLinks() {
    const tripResult = document.getElementById("tripResult");
    const links = tripResult.querySelectorAll('a[href*="localhost:8000/map"]');
    
    links.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const url = new URL(this.href);
            const destName = url.searchParams.get("dest_name");
            if (destName) {
                fetchLocation(destName);
                // Scroll to map section
                document.getElementById("map").scrollIntoView({ behavior: "smooth" });
            }
        });
    });
}