document.getElementById("chatForm").addEventListener("submit", async function(e){
    console.log("1 ok");
    e.preventDefault();
    console.log("2 ok");
    const resultDiv= document.getElementById("chatOutput");
    console.log("3 ok");
    resultDiv.innerHTML = "Thinking... Please wait. 🤔"; 
    console.log("4 ok");
    try{
        const formdata= new FormData();
        const response = await fetch("http://127.0.0.1:8000/chatbot/",{
            method:"POST",
            body: formdata
        });
        console.log(response);
        if (!reponse.ok) throw new Error("Server responded with an error");
        const result= await response.json();
        console.log(result);
        resultDiv.innerHTML= marked.parse(result.response)
    }
    catch(error){
        resultDiv.innerHTML= "Error:" + error.message;
    }
});