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
    $('#createUser').click(() => {
        $('#loginmodal').modal('hide')
        $('#usermodal').modal('show')
    })
});
