//Event listeners → Let JS respond to user actions (click, submit, hover, etc.)

document.getElementById("ImageSearchForm").addEventListener("submit", async function(event){
    console.log("by 1")
    event.preventDefault(); //Normally, submitting a form reloads the page and sends the data automatically. we prevent htis here
    console.log("by 2")
    const fileInput= document.getElementById("img");
    console.log(fileInput)
    const formData= new FormData(); //creates form ata object(this is for file inputs etc)
    console.log("by 3")
    formData.append("img", fileInput.files[0] );
    console.log(formData)
    const response = await fetch("http://127.0.0.1:8000/img_based_search/", {
        method: "POST",
        body: formData
    });
    console.log(response)
    const data= await response.json();
    console.log(data)
    const resultDiv= document.getElementById("imageResult");
    console.log("by 5")
    resultDiv.innerHTML=""; //Clears any previous results.
    resultDiv.style.display = "flex";
    resultDiv.style.flexWrap = "wrap";
    resultDiv.style.gap = "10px";
    console.log(resultDiv)
    data.results.forEach(item=>{  //Loops over each item in the results array.
        const container= document.createElement("div");
        container.style.textAlign = "center";
        container.style.flex = "0 0 auto";
        container.style.maxWidth = "220px";
        const title = document.createElement("h3");
        title.innerText= item.label;
        console.log(title)
        const img= document.createElement("img");
        img.src= item.image_url;
        console.log(img.src) 
        img.width = 200;
        img.height= 150;
        container.appendChild(title);
        console.log("by 6")
        container.appendChild(img);
        console.log("by 7")
        resultDiv.appendChild(container);
        console.log("by 7")

    })

})