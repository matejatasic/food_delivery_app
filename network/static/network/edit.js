const editRoute = "/edit"
const editDivs = document.getElementsByClassName("edit-div");
const editForms = document.getElementsByClassName("edit-form");
const editButtons = document.querySelectorAll(".edit-button");

editButtons.forEach(element => {
    element.addEventListener("click", (e) => {
        const id = e.target.id;
        const post_id = id.split("-")[2]
        
        const editDiv = document.getElementById(`edit-div-${post_id}`)
        const editForm = document.getElementById(`edit-form-${post_id}`);

        editDiv.style.display = "none";
        editForm.style.display = "block";
        
        const editSubmitButton = editForm.children[1];
        editSubmitButton.addEventListener('click', (e) => submitEdit(e, post_id, editForm, editDiv));
    })
});

function submitEdit(e, post_id, editForm, editDiv) {
    const textArea = editForm.children[0];
    const post = document.getElementById(`post-${post_id}`);
    
    fetch(`${editRoute}/${post_id}`, {
        method: "POST",
        body: JSON.stringify({
            content: textArea.value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.errors) {
            console.log(errors);
        }

        editDiv.style.display = "block";
        editForm.style.display = "none";

        post.textContent = textArea.value;
    })
    .catch(error => {
        console.log(error);
    }); 
}