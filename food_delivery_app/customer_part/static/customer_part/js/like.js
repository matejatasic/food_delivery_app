const likeButtons = document.querySelectorAll(".like-button");

likeButtons.forEach(element => {
    element.addEventListener("click", (e) => handleLikeButtonClick(e))
})

function handleLikeButtonClick(e) {
    const element = e.currentTarget
    restaurant_id = element.getAttribute("data-id");

    fetch(likeRoute, {
        method: "POST",
        body: JSON.stringify({
            restaurant_id: restaurant_id
        })
    })
    .then(res => res.json())
    .then(data => {
        changeLikeButtonIcon(element, data.action);
        changeLikeCount(element, data.current_number_of_likes);
    })
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