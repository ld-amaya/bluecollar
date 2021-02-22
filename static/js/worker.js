const album = document.querySelectorAll('.carousel-item')
let isDone ="no"
function loadActive() {
    album.forEach((image) => {
        if (isDone === "no"){
            image.classList.add('active')
            isDone = "yes"
        }
    })
}

loadActive()