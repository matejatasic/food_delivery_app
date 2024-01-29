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
    updateItemsListInHtml(itemId, data.cart);
    updateTotalItemQuantityInHtml(data.cart.total_number_of_items);
    updateExpensesInHtml(data["price_for_all_items"], data.delivery, data.tax, data.total);
}

function updateItemsListInHtml(itemId, cart) {
    const itemsListElement = document.getElementById("items-list");

    if (cart.total_number_of_items === 0) {
        itemsListElement.innerHTML = `<p class="text-center not-found">The cart is empty</p>`;
        return;
    }

    const cartItemsElements = document.querySelectorAll('.cart-item');

    if (Object.keys(cart.items).length === cartItemsElements.length) {
        updateItemQuantityInHtml(itemId, cart.items[itemId].quantity);

        return;
    }

    const listHtml = Object.values(cart.items).map(item =>
    `
        <div class="row cart-item border">
            <div class="col-2 d-flex justify-content-center align-items-center">
                <p>$${item.price}</p>
            </div>
            <div class="col-6 col-sm-6 p-2">
                <p class="cart-item-header">${item.name}</p>
                <p>${item.description}</p>
                <button class="btn btn-link increment-button" data-id="${item.id}"><i class="bi bi-plus-square-fill"></i></button>
                <span class="item-quantity" data-id="${item.id}">${item.quantity}</span>
                <button class="btn btn-link decrement-button" data-id="${item.id}"><i class="bi bi-file-minus-fill"></i></button>
            </div>
            <div class="col-4 col-sm-4">
                <img src="${mediaPrefix}${item.image}" alt="meal_image">
            </div>
        </div>
    `);

    itemsListElement.innerHTML = listHtml.join('');
    addEventListenersToChangeCartButtons(onSuccessCallback)
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

function updateExpensesInHtml(priceForAllItems, delivery, tax, total) {
    const decimalPlaces = 1

    document.getElementById("total-items-price").textContent = `$${priceForAllItems.toFixed(decimalPlaces)}`;
    document.getElementById("delivery").textContent = `$${delivery.toFixed(decimalPlaces)}`;
    document.getElementById("tax").textContent = `$${tax.toFixed(decimalPlaces)}`;
    document.getElementById("total").textContent = `$${total.toFixed(decimalPlaces)}`;
}
