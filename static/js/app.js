$(document).ready(function () {
    $('#login').click(() => {
        $('#loginmodal').modal('show')
    })
    $('#register').click(() => {
        $('#usermodal').modal('show')
    });

    $('#register_login').click(() => {
        $('#usermodal').modal('show')
    });

    $('#sendMessage').click(() => {
        if ($('#session').length) {
            console.log("You are in session")
        } else {
            console.log("You are NOT in session")
        }
    })

    
});
