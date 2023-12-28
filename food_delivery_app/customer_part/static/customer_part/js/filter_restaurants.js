const categoryButtons = document.querySelectorAll(".category-button");

categoryButtons.forEach(element => {
    element.addEventListener("click", (e) => handleCategoryButtonClick(e));
})

function handleCategoryButtonClick(e) {
    categoryName = e.currentTarget.getAttribute("data-name");

    fetch(
        `${getRestaurantsByCategoryRoute}?category_name=${categoryName}`,
        {
            method: "GET",
        }
    )
    .then(response => response.json())
    .then(response => {
        const data = JSON.parse(response.data);
        showFilteredRestaurants(data)
    })
}

function showFilteredRestaurants(data) {
    const restaurantsDiv = document.getElementById("restaurants");

    restaurantsDiv.innerHTML = "";

    data.forEach(restaurant => {
        restaurantsDiv.innerHTML += getRestaurantRow(restaurant, JSON.parse(restaurantsLikedByUser));
    })
}

function getRestaurantRow(restaurant, restaurantsLikedByUser) {
    let icon = '<i class="bi bi-hand-thumbs-up"></i>';

    if (restaurantsLikedByUser.includes(restaurant.id)) {
        icon = '<i class="bi bi-hand-thumbs-up-fill"></i>';
    }

    return `
        <div class="col-12" >
            <div class="row restaurant border">
                <div class="col-8 col-sm-8 p-2">
                    <p class="restaurant-header">${restaurant.name}</p>
                    <p>${restaurant.description}</p>
                    <span class="clickable like-button d-inline-block me-2 mt-2" data-id="{{ restaurant.id }}">
                        ${icon}
                    </span><span>${restaurant.number_of_likes}</span>
                </div>
                <div class="col-4 col-sm-4">
                    <img src="${mediaPrefix}${restaurant.image} " alt="restaurant_image">
                </div>
            </div>
        </div>
    `;
}