//this page includes favourite destinations 

document.addEventListener("DOMContentLoaded", async function(e){
    try{
        const mainDiv= document.getElementById("favList");

        const formdata= new FormData(e.target);

        const response= await fetch("http://127.0.0.1.8000/favDestination/get",{
         "body": formdata,
         "method": "GET",
         "credentials":"include"
         });
        const data= response.json();

        if(data!= null){

            console.log(data);

            mainDiv.appendChild(data);
            const del_button= document.createElement('button');
            const id= data['id'];
            const del_response= await fetch("http://127.0.0.1.8000/favDestination/delete/{id}",{
                "body": formdata,
                "method": "GET",
                "credentials":"include"
         });
         const del_data= del_response.json();
        }
        
            
        






        }catch(error){
            const no_destDiv= document.createElement("div");
            const para= document.createElement("p");
            para.innerText= "no favourite destinations has been saved";
            no_destDiv.appendChild(para);
        }



});