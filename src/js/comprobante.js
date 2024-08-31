$(document).ready(function() {
    // Cargar los tipos de comprobante en el select
    $.ajax({
        url: 'http://localhost:9000/tipo_comprobante',
        method: 'GET',
        success: function(response) {
            const tipoComprobanteSelect = $('#tipo_comprobante');
            response.forEach(function(tipo) {
                tipoComprobanteSelect.append(`<option value="${tipo.id_tipo_comprobante}">${tipo.nombre_comprobante}</option>`);
            });
        },
        error: function(error) {
            console.error('Error al cargar tipos de comprobante:', error);
        }
    });

    // Manejar el envío del formulario para crear un comprobante
    $('#crearComprobanteForm').submit(function(event) {
        event.preventDefault();

        const formData = new FormData(this);
        
        $.ajax({
            url: 'http://localhost:9000/comprobantes/crear',
            method: 'POST',
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                alert('Comprobante creado con éxito.');
                window.location.href = 'comprobante.html';
            },
            error: function(error) {
                console.error('Error al crear el comprobante:', error);
                alert('Hubo un error al crear el comprobante.');
            }
        });
    });
});
