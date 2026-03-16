document.getElementById("tripForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    console.log("1");
    const resultDiv = document.getElementById("tripResult");
    console.log("2");
    resultDiv.innerHTML = "Creating your Sri Lankan adventure... Please wait. 🐘"; // Loading state
    console.log("3");
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