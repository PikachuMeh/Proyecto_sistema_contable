$(document).ready(function () {
    let empresaSeleccionada = JSON.parse(localStorage.getItem('empresaSeleccionada'));
    let empresaId = empresaSeleccionada ? empresaSeleccionada.id : null;
    let asientoSeleccionado = localStorage.getItem('asientoSeleccionado');  // ID del asiento si lo tenemos

    // Verificar si tenemos un asiento específico seleccionado
    if (asientoSeleccionado) {
        cargarDetalleAsiento(asientoSeleccionado);
        cargarCuentasContables(empresaId);
    } else {
        cargarCuentasContables(empresaId);
        cargarAsientosEmpresa(empresaId);
    }

    // Función para cargar el detalle de un asiento específico
    function cargarDetalleAsiento(asientoId) {
        $.ajax({
            url: `http://localhost:9000/asientos?asiento_id=${asientoId}`,
            method: 'GET',
            success: function (response) {
                llenarDetalleAsiento(response);

                // Deshabilitar campos si el asiento está cerrado
                if (response.estado === 'Cerrado') {
                    deshabilitarFormulario();
                }
            },
            error: function (error) {
                console.error('Error al cargar los detalles del asiento:', error);
                alert('Hubo un problema al cargar los detalles del asiento.');
            }
        });
    }
    $('#agregar_cuenta_btn').click(function () {
        const cuentaId = $('#cuenta_contable').val();
        const tipoSaldo = $('#debe_haber').val();  
        const saldo = $('#monto').val();  
    
        if (!cuentaId || !tipoSaldo || !saldo) {
            alert("Todos los campos son obligatorios.");
            return;
        }

        $.ajax({
            url: `http://localhost:9000/asientos/${asientoSeleccionado}/cuentas`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                cuentaId: parseInt(cuentaId),
                tipo_saldo: tipoSaldo,
                saldo: parseFloat(saldo)
            }),
            success: function (response) {
                alert('Cuenta agregada con éxito');
                // Actualizar la lista de cuentas sin limpiar otras cuentas
                cargarDetallesActualizados(asientoSeleccionado);    
            },
            error: function (error) {
                console.error('Error al agregar la cuenta:', error);
                alert('Hubo un problema al agregar la cuenta.');
            }
        });
    });
    // Función para llenar los detalles de un asiento específico
    function llenarDetalleAsiento(asiento) {
        $('#detalle_num_asiento').text(`Número de Asiento: ${asiento.num_asiento || 'N/A'}`);
        $('#detalle_tipo_comprobante').text(`Tipo de Comprobante: ${asiento.tipo_comprobante || 'N/A'}`);
        $('#detalle_fecha_asiento').text(`Fecha del Asiento: ${asiento.fecha || 'N/A'}`);
        $('#estado_asiento').text(`Estado del Asiento: ${asiento.estado || 'N/A'}`);
        
        const listaCuentas = $('#lista_cuentas');
        listaCuentas.empty();  // Limpiar lista previa
        
        if (asiento.cuentas && asiento.cuentas.length > 0) {
            asiento.cuentas.forEach(cuenta => {
                const listItem = $(`
                    <li id="${cuenta.id}">
                        ${cuenta.nombre_cuenta} - ${cuenta.tipo_saldo.toUpperCase()} - ${cuenta.saldo}
                        ${asiento.estado !== 'Cerrado' ? `<button class="eliminar-cuenta-btn" data-id="${cuenta.id}">Eliminar</button>` : ''}
                    </li>
                `);
                listaCuentas.append(listItem);
            });
        } else {
            listaCuentas.append('<li>No hay cuentas asociadas con este asiento.</li>');
        }
    
        // Si el asiento está cerrado, deshabilitamos las acciones
        if (asiento.estado === 'Cerrado') {
            deshabilitarFormulario();  // Deshabilitar los botones para agregar cuentas y otros campos
        }
    }

    // Deshabilitar botones y campos cuando el asiento está cerrado
    function deshabilitarFormulario() {
        $('#agregar_cuenta_btn').prop('disabled', true);
        $('#cerrar_asiento_btn').prop('disabled', true);
        $('#cuenta_contable').prop('disabled', true);
        $('#debe_haber').prop('disabled', true);
        $('#monto').prop('disabled', true);
    }
    // Función para cargar las cuentas contables no principales
    function cargarCuentasContables(empresaId) {
        $.ajax({
            url: `http://localhost:9000/empresas/${empresaId}/cuentas_no_principales`,
            method: 'GET',
            success: function (response) {
                const cuentaContableSelect = $('#cuenta_contable');
                cuentaContableSelect.empty();
                response.forEach(cuenta => {
                    cuentaContableSelect.append(`<option value="${cuenta.id_cuenta_contable}">${cuenta.nombre_cuenta} (${cuenta.codigo})</option>`);
                });
            },
            error: function (error) {
                console.error('Error al cargar las cuentas contables:', error);
                alert('Error al cargar las cuentas contables.');
            }
        });
    }
    // Función para cargar todos los asientos de la empresa
    function cargarAsientosEmpresa(empresaId) {
        $.ajax({
            url: `http://localhost:9000/asientos?empresa_id=${empresaId}`,
            method: 'GET',
            success: function (response) {
                llenarAsientosEmpresa(response);
            },
            error: function (error) {
                console.error('Error al cargar los asientos de la empresa:', error);
                alert('Hubo un problema al cargar los asientos de la empresa.');
            }
        });
    }
     // Manejar la adición de cuentas al asiento
     

    // Función para manejar la eliminación de cuentas
    $('#lista_cuentas').on('click', '.eliminar-cuenta-btn', function () {
        const cuentaAsientoId = $(this).data('id');
        const asientoId = localStorage.getItem('asientoSeleccionado');
    
        if (confirm("¿Estás seguro de que deseas eliminar esta cuenta del asiento?")) {
            $.ajax({
                url: `http://localhost:9000/asientos/${asientoId}/cuentas/${cuentaAsientoId}`,
                method: 'DELETE',
                success: function (response) {
                    alert(response.mensaje);
                    cargarDetallesActualizados(asientoId);
                },
                error: function (error) {
                    console.error('Error al eliminar la cuenta:', error);
                    alert('Hubo un problema al eliminar la cuenta.');
                }
            });
        }
    });

    // Función para recargar los detalles del asiento
    function cargarDetallesActualizados(asientoId) {
        $.ajax({
            url: `http://localhost:9000/asientos?asiento_id=${asientoId}`,
            method: 'GET',
            success: function (response) {
                llenarDetalleAsiento(response);
            },
            error: function (error) {
                console.error('Error al cargar los detalles del asiento:', error);
                alert('Hubo un problema al cargar los detalles del asiento.');
            }
        });
    }

    // Botón para cerrar el asiento
    $('#cerrar_asiento_btn').click(function () {
        const asientoId = localStorage.getItem('asientoSeleccionado');
        
        $.ajax({
            url: `http://localhost:9000/asientos/${asientoId}/cerrar`,
            method: 'POST',
            success: function (response) {
                alert('Asiento cerrado con éxito.');
                localStorage.removeItem('asientoSeleccionado');
                window.location.href = 'generar_asientos.html';
            },
            error: function (error) {
                console.error('Error al cerrar el asiento:', error);
                if (error.responseJSON && error.responseJSON.detail) {
                    alert(`Error al cerrar el asiento: ${error.responseJSON.detail}`);
                } else {
                    alert('Hubo un problema al cerrar el asiento.');
                }
            }
        });
    });

    // Botón para volver a la página de generación de asientos
    $('#volver_btn').click(function () {
        window.location.href = 'generar_asientos.html';
    });
});