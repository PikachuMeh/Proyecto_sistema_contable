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

    // Cargar la empresa seleccionada desde localStorage
    const empresaSeleccionada = JSON.parse(localStorage.getItem('empresaSeleccionada'));
    if (empresaSeleccionada) {
        const empresaId = empresaSeleccionada.id;
        const empresaNombre = empresaSeleccionada.nombre;

        // Mostrar el nombre de la empresa en el título
        $('#empresa-nombre').text(empresaNombre);

        // Cargar los departamentos de la empresa seleccionada
        $.ajax({
            url: `http://localhost:9000/empresas/${empresaId}/departamentos`,
            method: 'GET',
            success: function(response) {
                const departamentoSelect = $('#departamento-select');
                departamentoSelect.empty(); // Limpiar el select antes de agregar nuevas opciones

                if (response.length > 0) {
                    // Rellenar el select con los departamentos
                    response.forEach(function(departamento) {
                        console.log("Departamento recibido:", departamento); // Asegúrate de ver ambos campos en consola
                        departamentoSelect.append(`<option value="${departamento.id_departamento}">${departamento.nombre_departamento}</option>`);
                    });

                    // Seleccionar la primera opción por defecto
                    departamentoSelect.val(departamentoSelect.find('option:first').val());
                    console.log("Departamentos cargados:", response);

                } else {
                    departamentoSelect.append('<option value="">No hay departamentos disponibles</option>');
                }

                // Mostrar qué opción está seleccionada por defecto
                console.log("Opción seleccionada inicialmente:", $('#departamento-select').val());
            },
            error: function(error) {
                console.error('Error al cargar los departamentos:', error);
                alert('Hubo un problema al cargar los departamentos. Intenta nuevamente.');
            }
        });

        // Manejo de la subida del archivo Excel
        $('#upload-plan-btn').click(function() {
            const archivo = $('#archivo-excel')[0].files[0];
            const departamentoIdStr = $('#departamento-select').val(); // Obtener el ID del departamento como string
            console.log("Valor bruto del departamento seleccionado:", departamentoIdStr);

            if (!departamentoIdStr || departamentoIdStr === "") {
                alert('Por favor, selecciona un departamento.');
                return;
            }

            const departamentoId = parseInt(departamentoIdStr, 10); // Convertir a entero
            console.log("Departamento seleccionado ID:", departamentoId);

            if (isNaN(departamentoId)) {
                alert('Por favor, selecciona un departamento válido.');
                return;
            }

            if (archivo) {
                const extension = archivo.name.split('.').pop().toLowerCase();
                if (extension !== 'xlsx') {
                    alert('Por favor, sube un archivo Excel con extensión .xlsx');
                    return;
                }

                const formData = new FormData();
                formData.append('archivo', archivo);
                formData.append('departamento_id', departamentoId); // Añadir el departamento al formData

                $.ajax({
                    url: `http://localhost:9000/empresas/${empresaId}/crear-plan/`,
                    method: 'POST',
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(response) {
                        if (response.resultados) {
                            alert('Plan de cuentas subido con éxito');
                            console.table(response.resultados);
                            window.location.replace('empresas.html');
                        } else {
                            alert('Error: no se recibieron resultados válidos.');
                            console.log('Respuesta incompleta o inesperada:', response);
                        }
                    },
                    error: function(error) {
                        const errorMessage = error.responseJSON?.detail || 'Hubo un error al subir el archivo. Intenta nuevamente.';
                        alert(errorMessage);
                        console.error('Error al subir el archivo:', error);
                    }
                });
            } else {
                alert('Por favor, selecciona un archivo');
            }
        });

    } else {
        alert('Por favor, selecciona una empresa primero.');
        window.location.replace('empresas.html');
    }
});
