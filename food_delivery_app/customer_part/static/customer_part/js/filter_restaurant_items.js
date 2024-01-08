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
}

function getItemRow(item) {
    return `
        <div class="col-12">
            <div class="row restaurant-item border">
                <div class="col-8 col-sm-8 p-2">
                    <p class="restaurant-item-header">${item.name}</p>
                    <p>${item.description}</p>
                    <button class="btn btn-link"><i class="bi bi-plus-square-fill"></i></button>
                </div>
                <div class="col-4 col-sm-4">
                    <img src="${mediaPrefix}${item.image}" alt="meal_image">
                </div>
            </div>
        </div>
    `;
}