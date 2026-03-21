document.getElementById("ImageSearchForm").addEventListener("submit", async function(e){
    //console.log("ok 1");
    e.preventDefault();
    //console.log("ok 2");
    const formData= new FormData(e.target);
    //console.log("ok 3");
    const resultDiv= document.getElementById("imageResult");
    resultDiv.innerHTML="Searching...";
    try{
        const response= await fetch(`${API_BASE}/img_based_search/`,{
            method:"POST",
            body:formData
        });
        //console.log("ok 4");
        if (!response.ok){
            throw new Error("Network response was not ok");
        }
        const data= await response.json();
        
        //console.log("ok 5");
        resultDiv.innerHTML="";
    
        //console.log("ok 6");
    
        //console.log("ok 7");
    
    
        data.results.forEach(item=>{

            const div = document.createElement("div");
            div.style.display = "inline-block";
            div.style.margin = "10px";

            const img= document.createElement("img");
            img.src= item.image_url;
            img.alt= item.label || "Image result";
            img.style.width= "200px";
            img.style.height= "150px";
            img.style.objectFit = "cover";

            const label = document.createElement("p");
            label.innerText = item.label || "Unknown";
            label.style.textAlign = "center";

            div.appendChild(img);
            div.appendChild(label);
            resultDiv.appendChild(div);
        
        });
    }catch(error){
        console.error("error:", error);
        resultDiv.innerText="Error: " + error.message;
    }

});