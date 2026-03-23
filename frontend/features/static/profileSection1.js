




document.addEventListener("DOMContentLoaded", async function() {
    try {
        const response = await fetch(`${API_BASE}/profile/`, {
            method     : "GET",
            credentials: "include"
        });

        if (response.status === 401) { handle401(); return; }
        if (!response.ok) throw new Error("Failed to load profile");

        const data = await response.json();
        document.getElementById("name").value  = data.name;
        document.getElementById("email").value = data.email;

    } catch(error) {
        showToast("❌ Failed to load profile", "error");
    }
});



//c.substring(name.length + 1) gets everything after the =.

//Example: "user_name=Nipuni" → "Nipuni"

//decodeURIComponent makes sure any URL-encoded characters (like %20) are converted back to normal characters.

//This returns the value of the cookie.

let originalName = "";


        
function editName() {
    const nameInput = document.getElementById("name");
    const editBtn   = document.getElementById("editName");

    
    originalName = nameInput.value; //save original name

    
    const nameDiv = document.createElement("div");
    nameDiv.id            = "editNameDiv";
    nameDiv.style.display = "flex";
    nameDiv.style.gap     = "8px";
    nameDiv.style.marginTop = "8px";

    
    const text   = document.createElement("input"); 
    text.type    = "text";
    text.value   = originalName;
    text.style.padding = "4px";

    
    const saveButton         = document.createElement("button");
    saveButton.innerHTML     = "✅ Save";
    saveButton.type          = "button";

   
    const cancelButton       = document.createElement("button");
    cancelButton.innerHTML   = "❌ Cancel";
    cancelButton.type        = "button";

    nameDiv.append(text);
    nameDiv.append(saveButton);
    nameDiv.append(cancelButton);

    
    nameInput.insertAdjacentElement("afterend", nameDiv);

   
    editBtn.style.display = "none"; //hide edit btn

    
    saveButton.addEventListener("click", async function(e) {
        e.preventDefault();
        const newName = text.value.trim();  

        //console.log(newName);

        if (!/^[a-zA-Z ]{3,}$/.test(newName)) {
            showToast("⚠️ Name must be at least 3 letters", "warning");
            return;
        }

        //console.log("hi 1");

        if (newName === originalName) {
            showToast("⚠️ Name is the same as current name", "warning");
            return;
        }
        //console.log("hi 2");

        try {
            const formdata = new FormData();
            formdata.append("new_name", newName);

            //console.log("hi 3");

            
            const response = await fetch(`${API_BASE}/profile/editName`, {
                method     : "PATCH",
                body       : formdata,
                credentials: "include"
            });

            //console.log("hi 4");

            if (response.status === 401) { handle401(); return; }
            //i created this handle401 function to handle session time out error, if 401 error happend user sees
            //a toast msg to log in again and redirect to login.html

            //console.log("hi 5");

            const data = await response.json();

            //console.log(response.status);

            if (response.ok) {
                
                nameInput.value = data.name;

                

                //console.log(nameInput);
                showToast("✅ Name updated successfully!", "success");
                cleanupEdit();
                //console.log("hi 7");
            } else {
                //console.log("hi 8");
                showToast("❌ " + (data.detail || "Failed to update name"), "error");
                //console.log("hi 9");
            }

        } catch(error) {
            //console.log("hi 10");
            showToast("❌ " + error.message, "error");
        }
    });

    
    cancelButton.addEventListener("click", function(e) {
        e.preventDefault();
        cleanupEdit();
    });
}

function cleanupEdit() {
    const nameDiv = document.getElementById("editNameDiv");
    const editBtn = document.getElementById("editName");

    if (nameDiv) if (nameDiv) nameDiv.remove();; 
    editBtn.style.display = "inline";
}                