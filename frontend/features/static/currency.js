let exchangeRates = {};

document.addEventListener("DOMContentLoaded", async function() {
    await fetchRates();

    // Trigger convert on amount input
    document.getElementById("currency-amount").addEventListener("input", convert);

    // Trigger convert when user selects from datalist
    document.getElementById("currency-search").addEventListener("input", convert);
    document.getElementById("currency-search").addEventListener("change", convert);
});

async function fetchRates() {
    const datalist  = document.getElementById("currency-list");
    const resultDiv = document.getElementById("currency-result");

    try {
        const response = await fetch("https://open.er-api.com/v6/latest/LKR");
        if (!response.ok) throw new Error("Failed to fetch rates");

        const data    = await response.json();
        exchangeRates = data.rates;

        // Populate datalist with all currencies
        datalist.innerHTML = "";
        Object.keys(data.rates).sort().forEach(code => {
            const option   = document.createElement("option");
            option.value   = code;
            datalist.appendChild(option);
        });

        //console.log(`Loaded ${Object.keys(data.rates).length} currencies`);

    } catch (error) {
        resultDiv.innerHTML = `<p style="color:red;">❌ Failed to load exchange rates. Please refresh.</p>`;
        showToast("❌ Failed to load exchange rates", "error");
    }
}

function convert() {
    const amount    = parseFloat(document.getElementById("currency-amount").value);
    const currency  = document.getElementById("currency-search").value.trim().toUpperCase();
    const resultDiv = document.getElementById("currency-result");

    if (!amount || isNaN(amount) || amount <= 0 || !currency) {
        resultDiv.innerHTML = "";
        return;
    }

    if (!exchangeRates[currency]) {
        resultDiv.innerHTML = `<p style="color:orange;">⚠️ Currency "${currency}" not found. Try USD, EUR, GBP...</p>`;
        return;
    }

    const rate      = exchangeRates[currency];
    const converted = (amount * rate).toFixed(2);

    resultDiv.innerHTML = `
        <div style="
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 16px;
            max-width: 350px;
            background: #f9f9f9;
            margin-top: 12px;
        ">
            <h3 style="margin:0 0 8px; color:#2E7D32;">
                LKR ${Number(amount).toLocaleString()} =
            </h3>
            <h2 style="margin:0; font-size:2rem; color:#1B5E20;">
                ${currency} ${converted}
            </h2>
            <hr style="margin:12px 0;">
            <p style="margin:0; color:#555; font-size:0.9rem;">
                1 ${currency} = LKR ${(1 / rate).toFixed(2)}
            </p>
            <p style="margin:4px 0 0; color:#aaa; font-size:0.8rem;">
                Rates updated daily · open.er-api.com
            </p>
        </div>
    `;
}