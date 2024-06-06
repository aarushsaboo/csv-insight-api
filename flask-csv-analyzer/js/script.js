const backendUrl = process.env.BACKEND_URL;

// Use the backendUrl in your JavaScript code
fetch(`${backendUrl}/api/data`)
  .then(response => response.json())
  .then(data => {
    // Handle the response data
    console.log(data);
  })
  .catch(error => {
    // Handle any errors
    console.error(error);
  });