document.getElementById("pdfForm").addEventListener("submit", async function(e){
    e.preventDefault();
    const text= document.getElementById("tripResult").innerText;
    if (!text || text.length < 10) {
        alert("Please generate a trip plan first!");
        return;
    }
    console.log(text);

    try{
        const response = await fetch("http://127.0.0.1:8000/pdf/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text }) // This matches your PDFRequest class
        });
        if (!response.ok) throw new Error("Backend failed to generate PDF");
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a= document.createElement("a");
        a.href= url;
        a.download= "trip_plan.pdf";
        document.body.appendChild(a);
        a.click();
    
        a.remove();
        window.URL.revokeObjectURL(url);
    }catch(error){
        alert("Error downloading PDF: " + error.message);
    }




});