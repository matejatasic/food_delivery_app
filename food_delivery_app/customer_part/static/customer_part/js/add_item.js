const INCREMENT = "increment";
const DECREMENT = "decrement";

function addEventListenersToChangeCartButtons(onSuccessCallback=null) {
    const incrementButtons = document.querySelectorAll(".increment-button");
    const decrementButtons = document.querySelectorAll(".decrement-button");

    incrementButtons.forEach(element => {
        element.addEventListener("click", (e) => handleChangeButtonsClick(e, INCREMENT, onSuccessCallback));
    })

    decrementButtons.forEach(element => {
        element.addEventListener("click", (e) => handleChangeButtonsClick(e, DECREMENT, onSuccessCallback));
    })
}

function handleChangeButtonsClick(e, action, onSuccessCallback) {
    const element = e.currentTarget;
    const itemId = element.getAttribute("data-id");

    addItemToCart(itemId, action, onSuccessCallback);
}

function addItemToCart(itemId, action, onSuccessCallback) {
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    fetch(changeCartUrl, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: JSON.stringify({
            item_id: itemId,
            action: action
        }),
    })
    .then(response => {
        if(!response.ok) {
            throw new Error(`HTTP status: ${response.status}`);
        }

        return response.json()
    })
    .then(response => {
        if (!onSuccessCallback) {
            return;
        }

        onSuccessCallback(itemId);
    })
    .catch(error => {
        console.log(error);
    });
}

export {addEventListenersToChangeCartButtons};
