document.getElementById("chatForm").addEventListener("submit", async function(e){
    e.preventDefault();
    const resultDiv= document.getElementById("chatOutput");
    resultDiv.innerHTML = "Thinking... Please wait. 🤔"; 
    try{
        const formdata= new FormData();
        const response = await fetch("http://127.0.0.1:8000/chatbot/",{
            method:"POST",
            body: formdata
        });
        if (!reponse.ok) throw new Error("Server responded with an error");
        const result= await response.json();
        resultDiv.innerHTML= marked.parse()
    }
    catch(error){
        resultDiv.innerHTML= "Error:" + error.message;
    }
});