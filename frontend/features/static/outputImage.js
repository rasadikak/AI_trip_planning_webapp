document.getElementById("tripForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // stop default form submission

    const tripResultDiv = document.getElementById("tripResult");
    tripResultDiv.innerHTML = "Generating your trip plan... ⏳"; // show loading

    try {
        const form = document.getElementById("tripForm");
        const formData = new FormData(form);

        const response = await fetch("http://127.0.0.1:8000/trip_planner/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        // Clear loading
        tripResultDiv.innerHTML = "";

        // Split the markdown text into lines for better display
        const lines = data["trip plan"].split("\n");

        lines.forEach(line => {
            const p = document.createElement("p");
            p.innerHTML = line || "<br>";
            tripResultDiv.appendChild(p);
        });

        // Optionally scroll to result
        tripResultDiv.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
        console.error("Error generating trip plan:", err);
        tripResultDiv.innerHTML = `<p style="color:red;">Error generating trip plan. Try again.</p>`;
    }
});