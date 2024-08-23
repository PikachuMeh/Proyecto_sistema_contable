$(document).ready(function() {
    // Manejar el cambio de opción
    $('input[name="plan-option"]').change(function() {
        if ($(this).val() === 'nuevo') {
            $('#crear-plan-form').show();
            $('#agregar-plan-form').hide();
        } else if ($(this).val() === 'archivo') {
            $('#crear-plan-form').hide();
            $('#agregar-plan-form').show();
        }
    });

    // Manejo de la subida del archivo Excel
    $('#upload-plan-btn').click(function() {
        const archivo = $('#archivo-excel')[0].files[0];
        
        if (archivo) {
            // Verificar que el archivo tenga la extensión correcta
            const extension = archivo.name.split('.').pop().toLowerCase();
            if (extension !== 'xlsx') {
                alert('Por favor, sube un archivo Excel con extensión .xlsx');
                return;
            }
    
            const formData = new FormData();
            formData.append('archivo', archivo);
    
            $.ajax({
                url: 'http://localhost:9000/empresas/crear-plan/', // Cambia a la ruta de tu API si es necesario
                method: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    // Manejar la respuesta exitosa
                    if (response.error) {
                        alert('Error: ' + response.error); // Mostrar mensaje de error específico
                    } else {
                        alert('Plan de cuentas subido con éxito');
                        console.log('Respuesta:', response);
                        window.location.replace('asientos_contables.html');
                    }
                },
                error: function(error) {
                    // Manejar errores
                    const errorMessage = error.responseJSON?.detail || 'Hubo un error al subir el archivo. Intenta nuevamente.';
                    alert(errorMessage);
                    console.error('Error al subir el archivo:', error);
                }
            });
        } else {
            alert('Por favor, selecciona un archivo');
        }
    });
});
