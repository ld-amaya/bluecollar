async function verifyEmail(email) {
    let res = await axios.get(`/email/${email}`)
    if (res.data.length > 0) {
        $('#email').val("")
        $('#emailtakenmodal').modal('show')
    }
}

$('#email').change(() => {
    verifyEmail($('#email').val())
})

