function get_cookie(name){
    let cookie=document.cookie.split(';');
    //document.cookie contains all cookies for the current page as a single string.
    //.split(";") turns it into an array of cookies:
     for (let i=0;i<cookie.length;i++){
        let c=cookie[i].trim(); //remove spaces
        if (c.startsWith(name + '=')){
            let value = decodeURIComponent(c.substring(name.length + 1));
            return value.replace(/^"|"$/g, ''); // removes starting/ending quotes
        }
     }
     //Loop through every cookie in the array.

    // .trim() removes spaces at the start or end (important because split creates spaces).
        return null; //if not found cookie 

};




document.addEventListener("DOMContentLoaded", function() {
    try{
    const name = get_cookie("user_name");
    const email = get_cookie("user_email");

    document.getElementById("name").value = name;
    document.getElementById("email").value = email;
    }catch(error){
        showToast("❌ Failed to load profile: " + error.message, "error");
    }
});



//c.substring(name.length + 1) gets everything after the =.

//Example: "user_name=Nipuni" → "Nipuni"

//decodeURIComponent makes sure any URL-encoded characters (like %20) are converted back to normal characters.

//This returns the value of the cookie.