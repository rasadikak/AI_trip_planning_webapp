window.addEventListener("load", () => {
    document.getElementById("ImageSearchForm").reset();
    document.getElementById("tripForm").reset();
    document.getElementById("weather_form").reset();

    document.getElementById("currency-amount").value = "";
    document.getElementById("currency-search").value = "";

    
    const currencyResult = document.getElementById("currency-result");
    if (currencyResult) currencyResult.innerHTML = "";
});




//above function -reset only works with forms