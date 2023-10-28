const likeRoute = "/like"
const likeButtons = document.querySelectorAll(".like-button");

likeButtons.forEach(element => {
    element.addEventListener("click", (e) => {
        const id = element.id;
        const post_id = id.split("-")[1]
        console.log(element.parentElement.children);
        fetch(likeRoute, {
            method: "POST",
            body: JSON.stringify({
                post_id: post_id
            })
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            let buttonSVG;

            if (data.action === "liked") {
                buttonSVG = '<i class="bi bi-suit-heart-fill">'
            }
            else {
                buttonSVG = '<i class="bi bi-suit-heart">'
            }

            element.parentElement.children[0].innerHTML = buttonSVG;
            
            const numberOfLikesSpan = element.parentElement.children[1]
            numberOfLikesSpan.textContent = data.current_number_of_likes;
        })
        .catch(error => {
            console.log(error);
        })
    })
});