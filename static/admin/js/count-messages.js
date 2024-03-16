function actualizarContadorMensajes() {
    $.ajax({
        url: '/dashboard/api/cantidad-mensajes/', // La URL del endpoint que devuelve la cantidad de mensajes
        type: 'GET',
        success: function(data) {
            $('#contador-mensajes').text(data.cantidad_mensajes); // Actualiza el contador
        }
    });
}

// Ejecuta la función de actualización cada 5 segundos
setInterval(actualizarContadorMensajes, 5000);