const URL ='https://raketraket.herukoapp.com'
const chat_container = document.getElementById('chat_container')
const chats = document.querySelectorAll('.chat')
    
async function loadMessages(id) {
    // Revisit this approach lou
    try {
        const response = await axios.get(`/messages/retrieve/${id}`)
        loadChat(response)
    } catch (e) {
        console.log(e)
    }
}

async function sendMessage() {
    try {
        params = {
            'id': $('#chatmate').data('id'),
            'text': $('#text').val()
        }
        const response = await axios.post('/messages/send', params)
        if (response.data.status != "False") {
            loadChat(response)    
        } else {
            window.location.href = `${URL}`
        }
    } catch (e) {
        console.log(e)
    }
}

async function checkMessages(id) {
    try {
        const response = await axios.get(`/checkunread/${id}`) 
        if (!response.data.read) {
            $(`#${id}`).addClass("font-weight-bold")
        }
    } catch (e) {
        console.log(e)
    }
}

function loadChat(response) {
    let text =''
    message = _.orderBy(response.data, 'id', 'asc')
    // add chatmate name
    $('#chat_header').html(`You and <span id='chatmate' data-id=${message[0].uid}> ${message[0].sender} </span>`)
    for (let i = 0; i < message.length; i++) {
        let timeStamp = getDate(message[i].timestamp)
        if ( message[i].sender == message[i].from) {
            text += `<div class="d-flex justify-content-end"> 
                        <div class ='text-from'>${message[i].message}</div> <br />
                    </div>
                    <div class='d-flex justify-content-end mb-2 sent'>${timeStamp}</div>`    
        } else {
            text += `<div class="justify-content-start mb-2">
                        <span class='text-you'>${message[i].message}</span>
                        <br/> <span class='sent'>${timeStamp}</span>
                    </div>`    
        }
    }
    $('#chat_container').html(text)
    $('#text').val("")
    bottomScroll()    
}

function getDate(thisDate) {
    timeStamp = moment(thisDate).fromNow()
    return timeStamp
}

function bottomScroll() {
    if (chat_container.scrollHeight){
        chat_container.scrollTop = chat_container.scrollHeight
    }
    
}

function checkUnread() {
    chats.forEach((chat) => {
        checkMessages(chat.id)        
    })
}

$('#sendMessage').click((e) => {
    if ($('#session').length) {
        $('#messagemodal').modal('show')
    } else {
        $('#loginTitle').html("You need to login before you send a message")
        $('#loginmodal').modal('show')
    }
})

$('.chat').click((e) => {
    e.preventDefault()
    loadMessages(e.target.id)
})

$('#send').click((e) => {
    if ($('#chatmate').data('id')) {
        sendMessage()
    }
})
if (chat_container) {
    bottomScroll()    
}
checkUnread()