import { addEventListenersToChangeCartButtons } from "./add_item.js";

addEventListenersToChangeCartButtons(onSuccessCallback)

function onSuccessCallback(itemId) {
    fetch(getCartUrl, {
        method: "GET",
    })
    .then(response => {
        if(!response.ok) {
            throw new Error(`HTTP status: ${response.status}`);
        }

        return response.json()
    })
    .then(response => {
        const data = JSON.parse(response.data);

        updateHtml(itemId, data);

    })
    .catch(error => {
        console.log(error);
    });
}

function updateHtml(itemId, data) {
    updateTotalItemQuantityInHtml(data.cart.total_number_of_items);
    updateItemQuantityInHtml(itemId, data.cart.items[itemId].quantity);
}

function updateTotalItemQuantityInHtml(totalNumberOfItems) {
    const cartQuantityElement = document.getElementById("cart-quantity");
    cartQuantityElement.textContent = totalNumberOfItems;
}

function updateItemQuantityInHtml(itemId, quantity) {
    const quantitySpan = document.querySelector(`.item-quantity[data-id='${itemId}']`);

    if (!quantitySpan) {
        return;
    }

    if (quantity === 0) {
        quantitySpan.textContent = "";

        return;
    }

    quantitySpan.textContent = quantity;
}
