const URL = "https://raketraket.herokuapps.com"

async function loadCities() {
    try {
        const response = await axios.get(`${URL}/cities`)
        cities = response.data.cities
        cities.forEach((city) => {
            $('#cities').append(`<option value=${city.id}>${city.city}</option>`)
        })

        services = response.data.services
        services.forEach((service) => {
            s = service.toLowerCase()
            $(`#${s}`).attr('checked', 'True')
        }
        )
        $('#cities').val(response.data.user.id)
        
    } catch (e) {
        console.log(e)
    }
    
}
loadCities()