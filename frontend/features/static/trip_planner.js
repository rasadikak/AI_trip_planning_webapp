// Get references to the form and result div
const form = document.getElementById('ImageSearchForm');
const resultDiv = document.getElementById('imageResult');

// Listen for form submission
form.addEventListener('submit', async (e) => {
  e.preventDefault(); // prevent page reload

  const fileInput = document.getElementById('destImage');
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image!");
    return;
  }

  // Prepare FormData to send to FastAPI
  const formData = new FormData();
  formData.append('img', file); // 'img' matches FastAPI parameter name

  try {
    // Send image to FastAPI endpoint
    const response = await fetch('http://127.0.0.1:8000/img_based_search/', {
      method: 'POST',
      body: formData
    });

    // Get JSON result
    const data = await response.json();

    // Clear previous results
    resultDiv.innerHTML = '';

    // Loop through returned images and display
    data.results.forEach(item => {
      // Create container div
      const container = document.createElement('div');
      container.style.display = 'inline-block';
      container.style.textAlign = 'center';
      container.style.margin = '10px';

      // Create image element
      const imgElem = document.createElement('img');
      imgElem.src = item.image_url; // URL returned by FastAPI
      imgElem.alt = item.label;
      imgElem.style.width = '200px';
      imgElem.style.height = 'auto';
      imgElem.style.border = '1px solid #ccc';
      imgElem.style.borderRadius = '5px';

      // Create label element
      const labelElem = document.createElement('p');
      labelElem.textContent = item.label;
      labelElem.style.marginTop = '5px';
      labelElem.style.fontWeight = 'bold';

      // Append image and label to container
      container.appendChild(imgElem);
      container.appendChild(labelElem);

      // Append container to result div
      resultDiv.appendChild(container);
    });

  } catch (err) {
    console.error(err);
    alert("Error searching image. Make sure FastAPI is running and the endpoint is correct.");
  }
});