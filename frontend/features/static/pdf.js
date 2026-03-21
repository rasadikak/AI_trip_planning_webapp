document.addEventListener("DOMContentLoaded", function() {
 document.getElementById("pdfForm").addEventListener("submit", async function(e){
    //console.log("PDF form submitted");
    e.preventDefault();
    //console.log("Fetching trip plan text for PDF generation...");
    const text= document.getElementById("tripResult").innerText;
    if (!text || text.length < 10) {
        showToast("⚠️ Please generate a trip plan first!", "warning");
        return;
    }
    //console.log(text);
    try{
        const response = await fetch(`${API_BASE}/pdf/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text }) // This matches your PDFRequest class
        });
        //console.log("PDF generation response received");
        if (!response.ok) throw new Error("Backend failed to generate PDF");
        //console.log("Processing PDF blob...");
        const blob = await response.blob();
        //console.log("PDF blob created, initiating download...");
        const url = window.URL.createObjectURL(blob);
        //console.log("Download URL created: ", url);
        const a= document.createElement("a");
        a.href= url;
        //console.log("Anchor element created for download");
        a.download= "trip_plan.pdf";
        //console.log("Anchor element configured for download");
        document.body.appendChild(a);
        //console.log("Anchor element added to DOM, triggering click...");
        a.click();
        //console.log("Download triggered, cleaning up...");
        a.remove();
        //console.log("Anchor element removed, revoking URL...");
        window.URL.revokeObjectURL(url);
        showToast("📄 PDF downloaded successfully!", "success");
    }catch(error){
        console.error("Error:", error);
        showToast("Error downloading PDF: " + error.message, "error");
    }
})});