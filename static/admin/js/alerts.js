
document.addEventListener("DOMContentLoaded", function () {
    // Cierra las alertas después de 5 segundos (5000 milisegundos)
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 5000);
});
