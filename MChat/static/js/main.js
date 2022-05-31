const roofName = JSON.parse(document.getElementById('roof-name').textContent);
const user_id = JSON.parse(document.getElementById('user_id').textContent);
const user_img = JSON.parse(document.getElementById('user_img').textContent);
const user_nick = JSON.parse(document.getElementById('user_nick').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roofName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    html = generate_chat_log(data);

    document.getElementById("chat-log").insertAdjacentHTML('beforeend', html);


};

function generate_chat_log(data) {
    const data_user_id = data.user_id;
    var data_user_img = '/media/' + data.user_img;
    const data_message = data.message;
    var data_timestamp = data.timestamp;
    const data_user_nick = data.user_nick;


    if (data.user_img == null || data.user_img === '')
    {
        data_user_img = '/media/images/no-image.jpeg';
    }

    data_timestamp = epochToJsDate(data_timestamp/1000).toLocaleString();

    let html;
    if (data_user_id === user_id) {
        // Mensaje propio
        html =
            '<div class="d-flex flex-row justify-content-end mb-4">' +
            '<div class="p-3 me-3 border michi-color chat-text-right" >' +
            '<p class="small mb-0 text-break">' + data_message + '</p>' +
            '<p class="text-muted text-end mb-0 mt-2" style="font-size: xx-small">Enviado el ' + data_timestamp + '</p>' +
            '<p class="text-muted text-end mb-0 mt-2" style="font-size: xx-small">Por <a href="'+
                window.location.protocol +'//'+window.location.hostname+':'+window.location.port+'/view_profile/'+data_user_id+'/">' + data_user_nick + '</a></p>' +
            '</div>' +
            '<img class="img-responsive" src="' + data_user_img + '" alt="avatar 1">' +
            '</div>';

    } else {
        // Mensaje de otro
        html =
            '<div class="d-flex flex-row justify-content-start mb-4">' +
            '<img class="img-responsive" src="' + data_user_img + '"  alt="avatar 1" >' +
            '<div class="p-3 ms-3 michi-color chat-text-left">' +
            '<p class="small mb-0 text-break">' + data_message + '</p>' +
            '<p class="text-muted text-start mb-0 mt-2" style="font-size: xx-small">Enviado el ' + data_timestamp + '</p>' +
            '<p class="text-muted text-start mb-0 mt-2" style="font-size: xx-small">Por <a href="'+
                window.location.protocol +'//'+window.location.hostname+':'+window.location.port+'/view_profile/'+data_user_id+'/">' + data_user_nick + '</a></p>' +
            '</div>' +
            '</div>';
    }

    return html;

}

function epochToJsDate(ts){
    return new Date(ts*1000);
}

function scrollToBottom() {
    const chatLog = document.getElementById('chat-log');
    chatLog.scrollTop = chatLog.scrollHeight;
}



chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    if (message.trim() === '') {
        return;
    }

    chatSocket.send(JSON.stringify({
        'message': message,
        'user_id': user_id,
        'user_nick': user_nick,
        'user_img': user_img,
        'timestamp': new Date().getTime()
    }));
    messageInputDom.value = '';
};

