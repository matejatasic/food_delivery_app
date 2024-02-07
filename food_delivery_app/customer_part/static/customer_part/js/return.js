import { updateTotalItemQuantityInHtml } from "./cart.js";

initialize();

async function initialize() {
  let response = await fetch(`${stripeSessionStatusUrl}?session_id=${sessionId}`);
  const session = await response.json();
  const messageElement = document.getElementById("message");

  if (session.status == 'open') {
    window.location.href = cartUrl;
  } else if (session.status == 'complete') {
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    response = await fetch(createOrderUrl, {
        "method": "POST",
        headers: { "X-CSRFToken": csrfToken }
    });

    updateTotalItemQuantityInHtml(0);

    if(response.status !== 200) {
        messageElement.textContent = "There was a server error";
    }
    else {
      messageElement.textContent = "Thank you for your purchase! A driver will soon pick up your order.";
    }
  }
  else {
    messageElement.textContent = session.message;
  }

  document.getElementById('response-div').classList.remove('hidden');
}