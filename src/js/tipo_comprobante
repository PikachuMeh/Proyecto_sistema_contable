$(document).ready(function() {
    // Cargar la lista de tipos de comprobante
    function cargarTiposComprobante() {
        $.ajax({
            url: 'http://localhost:9000/tipo_comprobante',
            method: 'GET',
            success: function(response) {
                const lista = $('#lista-tipos-comprobante');
                lista.empty();
                response.forEach(function(tipo) {
                    lista.append(`<li>${tipo.nombre_comprobante}</li>`);
                });
            },
            error: function(error) {
                console.error('Error al cargar tipos de comprobante:', error);
            }
        });
    }

    cargarTiposComprobante();

    // Manejar el envío del formulario para crear un tipo de comprobante
    $('#crearTipoComprobanteForm').submit(function(event) {
        event.preventDefault();

        const nombreComprobante = $('#nombre_comprobante').val();

        $.ajax({
            url: 'http://localhost:9000/tipo_comprobante/crear',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ nombre_comprobante: nombreComprobante }),
            success: function(response) {
                alert('Tipo de comprobante creado con éxito.');
                cargarTiposComprobante();
            },
            error: function(error) {
                console.error('Error al crear el tipo de comprobante:', error);
                alert('Hubo un error al crear el tipo de comprobante.');
            }
        });
    });
});
