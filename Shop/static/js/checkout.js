document.getElementById("checkout-button").addEventListener("click", function() {
    let phoneNumber = document.querySelector("input[name='phone_number']").value;
    let shippingAddress = document.querySelector("input[name='shipping_address']").value;

    // Get CSRF token from the DOM and include it in the headers
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.location.pathname, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken, // Add the CSRF token here
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            phone_number: phoneNumber,
            shipping_address: shippingAddress
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            var stripe = Stripe(""); // For Checkout Insert Your Stripe Publishable Key Here
            stripe.redirectToCheckout({ sessionId: data.session_id });
        }
    })
    .catch(error => console.error("Payment failed:", error));
});
