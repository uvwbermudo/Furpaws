var socket;

$(document).ready(function(){
    console.log('READY2')
    const socket_add = $('#socket_add').val()
    const flask_port= $('#flask_port').val()
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    sessionStorage.setItem('socket', JSON.stringify(user));
    console.log(socket)
});

function get_socket(){
    console.log('HEY')
    console.log(socket)
    return socket;
}