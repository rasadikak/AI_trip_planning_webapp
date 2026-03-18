document.getElementById("ImageSearchForm").addEventListener("submit", async function(e){
    e.preventDefault();
    const formData= new FormData(e.target);
    const response= await fetch("http://127.0.0.1:8000/img_based_search/",{
        method:"POST",
        body:formData
    });
    const resultDiv= document.getElementById("imageResult");
    if (!response.ok){
        throw new Error("Network response was not ok");
    }
    const data= await response.json();
    resultDiv.innerHTML="";
    data.forEach=>(item=>{
        const img= document.createElement("img");
        img.src= item.image_url;
        img.alt= item.label || "Image result";
        img.style.width= "200px";
        img.style.height= "150px";
        img.
        
    });
    resultDiv.appendChild(img);

});