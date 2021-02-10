function clearRates() {
    for (let i = 1; i < 6; i++){
        $(`#rate${i}`).removeClass('fas')
    }    
}

function addStar(rate) {
    for (let i = 1; i <= rate; i++){
        $(`#rate${i}`).addClass('fas')
    }
}

// Rating and Comments
$('#rateandcomment').click(() => {
    if ($('#session').length) {
        $('#commentmodal').modal('show')
    } else {
        $('#loginTitle').html("<h5>Login to Comment and Rate</h5>")
        $('#loginmodal').modal('show')
    }
})

// Change star color on mouseover 
$('.far').mouseover((e) => {
    rating = e.target.dataset.rate
    label = e.target.dataset.label
    clearRates()
    addStar(rating)
    $('#yourRate').html(label)
})

// Return star color to default leaving the current rating as colored
$('.far').mouseleave(() => {
    rating = $('.rating').val()
    for (i = 1; i <= 5; i++){
        $(`#rate${i}`).removeClass('fas')
    }
    for (i = 1; i <= rating; i++){
        $(`#rate${i}`).addClass('fas')
    }
})

// Store star rating to a hidden input element
$('.rate').click((e) => {
    rating = e.target.dataset.rate 
    $('.rating').val(rating)
})