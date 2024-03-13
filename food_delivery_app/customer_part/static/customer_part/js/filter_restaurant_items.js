import { addEventListenersToChangeCartButtons } from "./add_item.js";

const categoryButtons = document.querySelectorAll(".category-button");

categoryButtons.forEach(element => {
    element.addEventListener("click", (e) => handleCategoryButtonClick(e));
})

function handleCategoryButtonClick(e) {
    const categoryName = e.currentTarget.getAttribute("data-name");

    fetch(
        `${getRestaurantItemsByCategoryUrl}?category_name=${categoryName}`,
        {
            method: "GET",
        }
    )
    .then(response => response.json())
    .then(response => {
        const data = JSON.parse(response.data);
        showFilteredRestaurants(data);
    })
}

function showFilteredRestaurants(data) {
    const restaurantsDiv = document.getElementById("items");

    restaurantsDiv.innerHTML = "";

    data.forEach(item => {
        restaurantsDiv.innerHTML += getItemRow(item);
    })
    addEventListenersToChangeCartButtons()
}

function getItemRow(item) {
    let changeCartButtons = "";

    if (isUserAuthenticated === "True") {
        changeCartButtons = `
            <button class="btn btn-link decrement-button" data-id="${item.id}"><i class="bi bi-dash-square-fill"></i></button>
            <button class="btn btn-link increment-button" data-id="${item.id}"><i class="bi bi-plus-square-fill"></i></button>
        `;
    }

    return `
        <div class="col-12">
            <div class="row restaurant-item border">
                <div class="col-8 col-sm-8 p-2">
                    <p class="restaurant-item-header">${item.name}</p>
                    <p>${item.description}</p>

                    ${changeCartButtons}
                </div>
                <div class="col-4 col-sm-4">
                    <img src="${mediaPrefix}restaurant_items/${item.image}" alt="meal_image">
                </div>
            </div>
        </div>
    `;
}