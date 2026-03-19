document.addEventListener('DOMContentLoader', async function(e){
    try{

    e.preventDefault();
    const formdata=new FormData(e.target);
    const response= await fetch('http://127.0.0.1:8000/savedPlans',{
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
    planList.innerText="";

    data.response.forEach(item=>{
        const div= document.createElement("div");
        console.log("item:", item);
            
        div.style.border = "1px solid #ccc";
        div.style.padding = "10px";
        div.style.marginBottom = "10px";

        div.innerHTML = `
                <h3>📍 ${item.destination}</h3>
                <p> ${item.plan}</p>
                <p> ${new Date(item.created_at).toLocaleDateString()}</p>
                <button onclick="deletePlan(${item.id})">🗑️ Remove plan</button>
            `;

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