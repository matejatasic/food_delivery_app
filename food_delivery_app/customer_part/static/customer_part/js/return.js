import { updateTotalItemQuantityInHtml } from "./cart.js";

initialize();

async function initialize() {
  let response = await fetch(`${stripeSessionStatusUrl}?session_id=${sessionId}`);
  const session = await response.json();

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
        console.log("There was an error");
        return;
    }

    document.getElementById('success').classList.remove('hidden');
  }
}