const incrementButtons = document.querySelectorAll(".increment-button");
const decrementButtons = document.querySelectorAll(".decrement-button");

const INCREMENT = "increment";
const DECREMENT = "decrement";

incrementButtons.forEach(element => {
    element.addEventListener("click", (e) => handleChangeButtonsClick(e, INCREMENT));
})

decrementButtons.forEach(element => {
    element.addEventListener("click", (e) => handleChangeButtonsClick(e, DECREMENT));
})

function handleChangeButtonsClick(e, action) {
    const element = e.currentTarget;
    const itemId = element.getAttribute("data-id");

    fetch(changeCartUrl, {
        method: "POST",
        body: JSON.stringify({
            item_id: itemId,
            action: action
        })
    })
    .then(res => res.json())
    .then(response => {
        const cartQuantityElement = document.getElementById("cart-quantity");
        cartQuantityElement.textContent = JSON.parse(response.data).total_number_of_items;
    });
}