$(document).ready(function () {
    // Obtener el id del asiento desde la URL
    const params = new URLSearchParams(window.location.search);
    const asientoId = params.get('asiento_id');
    let empresaSeleccionada = JSON.parse(localStorage.getItem('empresaSeleccionada'));
    let empresaId = empresaSeleccionada ? empresaSeleccionada.id : null;

    if (!asientoId) {
        alert("No se ha proporcionado un ID de asiento.");
        return;
    }

    // Cargar los detalles del asiento contable
    $.ajax({
        url: `http://localhost:9000/asientos/${asientoId}`,
        method: 'GET',
        success: function (response) {
            mostrarDetalleAsiento(response);
        },
        error: function (error) {
            console.error('Error al cargar el asiento:', error);
            alert('Hubo un problema al cargar el asiento.');
        }
    });

    // Cargar las cuentas contables no principales para seleccionar
    cargarCuentasContables(empresaId);

    // Función para mostrar los detalles del asiento
    function mostrarDetalleAsiento(asiento) {
        $('#detalle_num_asiento').text(`Número de Asiento: ${asiento.num_asiento}`);
        $('#detalle_tipo_comprobante').text(`Tipo de Comprobante: ${asiento.tipo_comprobante}`);
        $('#detalle_fecha_asiento').text(`Fecha del Asiento: ${asiento.fecha}`);
    
        const listaCuentas = $('#lista_cuentas');
        listaCuentas.empty();
    
        if (Array.isArray(asiento.cuentas)) {
            asiento.cuentas.forEach(cuenta => {
                listaCuentas.append(`<li>${cuenta.nombre_cuenta} - ${cuenta.tipo_saldo} - ${cuenta.saldo}</li>`);
            });
        } else {
            listaCuentas.append('<li>No hay cuentas asociadas con este asiento.</li>');
        }
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
    $('#cerrar_asiento_btn').click(function () {
        $.ajax({
            url: `http://localhost:9000/asientos/${asientoId}/cerrar`,
            method: 'POST',
            success: function (response) {
                alert(response.mensaje);
                // Desactivar los botones y formularios de edición
                $('#agregar_cuenta_btn').prop('disabled', true);
                $('#cerrar_asiento_btn').prop('disabled', true);
            },
            error: function (error) {
                console.error('Error al cerrar el asiento:', error);
                alert('Hubo un problema al cerrar el asiento: ' + error.responseJSON.detail);
            }
        });
    });
    // Manejar la adición de cuentas al asiento
    $('#agregar_cuenta_btn').click(function () {
        const cuentaId = $('#cuenta_contable').val();
        const tipoSaldo = $('#debe_haber').val();  // Ajustar el ID si es necesario
        const saldo = $('#monto').val();  // Ajustar el ID si es necesario
    
        if (!cuentaId || !tipoSaldo || !saldo) {
            alert("Todos los campos son obligatorios.");
            return;
        }
    
        $.ajax({
            url: `http://localhost:9000/asientos/${asientoId}/cuentas`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                cuentaId: parseInt(cuentaId),
                tipo_saldo: tipoSaldo,
                saldo: parseFloat(saldo)
            }),
            success: function (response) {
                alert('Cuenta agregada con éxito');
                mostrarDetalleAsiento(response);
            },
            error: function (error) {
                console.error('Error al agregar la cuenta:', error);
                alert('Hubo un problema al agregar la cuenta.');
            }
        });
    });
    

    // Botón para volver a la página de generación de asientos
    $('#volver_btn').click(function () {
        window.location.href = 'generar_asientos.html';
    });
});
