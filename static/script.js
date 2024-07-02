function registerForTrip(rideId) {
    // Make an API request to your Flask route for user registration
    // You can use the fetch API or any other AJAX library
    // Example using fetch:
    fetch('/register_trip', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rideId: rideId })
    })
    .then(response => response.json())
    .then(data => {
        // Handle success or error messages
        alert(data.message);
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// function doFunction() {
//     // Your registration logic here
//     // For example, show a registration form or send an API request
//     // You can also redirect the user to a registration page using window.location.href
//     alert("Button clicked!"); // Replace with your actual logic
// }

function redirectToRegistration() {
    // Redirect to the registration page
    window.location.href = "{{ url_for('register') }}"; // Replace with your actual registration page URL
}