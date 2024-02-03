const STRIPE_PUBLIC_KEY = document.getElementById("stripe-public-key").value;
const stripe = Stripe(STRIPE_PUBLIC_KEY);

const checkoutButton = document.getElementById("checkout-button");
if (checkoutButton) {
  checkoutButton.addEventListener("click", () => initialize());
}

async function initialize() {
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  const response = await fetch(createCheckoutSessionUrl, {
    headers: { "X-CSRFToken": csrfToken },
    method: "POST",
  });

  if (response.status === 500) {
    console.log("There was a server error");
    return;
  }

  const { clientSecret } = await response.json();

  const checkout = await stripe.initEmbeddedCheckout({
    clientSecret,
  });

  checkout.mount('#checkout');
}
