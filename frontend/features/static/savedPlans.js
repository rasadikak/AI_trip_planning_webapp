document.addEventListener('DOMContentLoaded', async function(e){
    try{

   
    const response= await fetch('http://127.0.0.1:8000/savedPlans/get',{
        "method":"GET",
        "credentials":"include"
    });

    if (!response.ok) throw new Error("Failed to load: " + response.status);
    const data= await response.json();

    if (!data || !data.response || data.response.length === 0) {
            favList.innerHTML = "<p>No saved plans yet.</p>";
            return;
}

    const planList = document.getElementById("planList");
    planList.innerHTML="";

    data.response.forEach(item => {
    const div = document.createElement("div");
    div.style.border = "1px solid #ccc";
    div.style.padding = "10px";
    div.style.marginBottom = "10px";

    // Store plan in data attribute to avoid breaking onclick
    const downloadBtn = document.createElement("button");
    downloadBtn.innerText = "📄 Download PDF";
    downloadBtn.onclick = () => downloadPDF(item.plan);  // pass directly via closure

    const deleteBtn = document.createElement("button");
    deleteBtn.innerText = "🗑️ Remove Plan";
    deleteBtn.onclick = () => deletePlan(item.id);

    div.innerHTML = `
        <h3>📍 ${item.destination}</h3>
        <div>${marked.parse(item.plan)}</div>
        <p>Saved on: ${new Date(item.created_at).toLocaleDateString()}</p>
    `;

    div.appendChild(deleteBtn);
    div.appendChild(downloadBtn);
    planList.appendChild(div);
});
    }catch(error){
        console.error("Error:", error);
        planList.innerHTML = "<p>Error loading saved plans: " + error.message + "</p>";
    }
});



async function deletePlan(plan_id){
    try{
        const response = await fetch(`http://127.0.0.1:8000/savedPlans/delete/${plan_id}`, {
            method: "DELETE",
            credentials: "include"
        });
        console.log("delete response:", response.status);

        if (!response.ok) throw new Error("Failed to delete");

        alert("deleted successfully!");
        location.reload(); 

}catch(error){
    alert("can not delete plan:", error.message)
}
}




async function downloadPDF(plan){
    
    
    
    try{
        const response = await fetch("http://127.0.0.1:8000/pdf/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: plan })
        });
        console.log("PDF generation response received");
        if (!response.ok) throw new Error("Backend failed to generate PDF");
        console.log("Processing PDF blob...");
        const blob = await response.blob();
        console.log("PDF blob created, initiating download...");
        const url = window.URL.createObjectURL(blob);
        console.log("Download URL created: ", url);
        const a= document.createElement("a");
        a.href= url;
        console.log("Anchor element created for download");
        a.download= "trip_plan.pdf";
        console.log("Anchor element configured for download");
        document.body.appendChild(a);
        console.log("Anchor element added to DOM, triggering click...");
        a.click();
        console.log("Download triggered, cleaning up...");
        a.remove();
        console.log("Anchor element removed, revoking URL...");
        window.URL.revokeObjectURL(url);
    }catch(error){
        alert("Error downloading PDF: " + error.message);
    }






}