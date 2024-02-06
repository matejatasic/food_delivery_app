addEventListenersToLikeButtons();

function addEventListenersToLikeButtons() {
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach(element => {
        element.addEventListener("click", (e) => handleLikeButtonClick(e))
    })
}

function handleLikeButtonClick(e) {
    const element = e.currentTarget
    const restaurantId = element.getAttribute("data-id");
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    fetch(likeRoute, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: JSON.stringify({
            restaurant_id: restaurantId
        })
    })
    .then(res => res.json())
    .then(data => {
        changeLikeButtonIcon(element, data.action);
        changeLikeCount(element, data.current_number_of_likes);
    });
}

function changeLikeButtonIcon(element, actionTaken) {
    let buttonIcon;

    if (actionTaken === "liked") {
        buttonIcon = '<i class="bi bi-hand-thumbs-up-fill">';
    }
    else {
        buttonIcon = '<i class="bi bi-hand-thumbs-up">';
    }

    element.innerHTML = buttonIcon;
}

function changeLikeCount(element, currentNumberOfLikes) {
    const numberOfLikesSpan = element.nextElementSibling;
    numberOfLikesSpan.textContent = currentNumberOfLikes;
}

export {addEventListenersToLikeButtons};