//Event listeners → Let JS respond to user actions (click, submit, hover, etc.)

document.getElementById("ImageSearchForm").addEventListener("submit", async function(event){
    event.preventDefault(); //Normally, submitting a form reloads the page and sends the data automatically. we prevent htis here
    const fileInput= document.getElementById("img");
    const formData= new FormData(); //creates form ata object(this is for file inputs etc)
    formData.append("img", fileInput.files[0] );
    const response = await fetch("http://127.0.0.1:8000/img_based_search/", {
        method: "POST",
        body: formData
    });
    const data= response.json();
    const resultDiv= document.getElementById("result");
    resultDiv.innerHTML=""; //Clears any previous results.
    data.results.foeEach(item=>{  //Loops over each item in the results array.
        const container= documnet.createElement("div");
        const title = document.createElement("h3");
        title.innerText= item.label;
        const img= documnet.createElement("img");
        img.src= item.image_url;
        img.width = 200;
        container.appendChild(title);
        container.appendChild(img);
        resultDiv.appendChild(container);

    })

})