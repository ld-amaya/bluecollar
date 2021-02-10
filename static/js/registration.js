const URL = "http://127.0.0.1:5000"


async function verifyEmail(email) {
    let res = await axios.post(`${URL}/email/${email}`)
    if (res.data.length > 0) {
        $('#email').val("")
        $('#emailtakenmodal').modal('show')
    }
}

$('#email').change(() => {
    verifyEmail($('#email').val())
})

