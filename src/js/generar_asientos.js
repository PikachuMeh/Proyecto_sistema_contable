$(document).ready(function () {
    // Cargar tipos de comprobante al inicio
    cargarTiposDeComprobante();
    cargarAsientosContables();

    // Manejar la creación de un nuevo asiento contable
    $('#crear_asiento_btn').click(function () {
        const numAsiento = $('#num_asiento').val();
        const tipoComprobanteId = $('#tipo_comprobante').val();
        const fechaAsiento = $('#fecha_asiento').val();
        const documentoRespaldo = $('#documento_respaldo')[0].files[0];

        // Validar que el número de asiento sea positivo
        if (numAsiento <= 0 || isNaN(numAsiento)) {
            alert('El número de asiento debe ser un número positivo.');
            return;
        }
        if (!numAsiento || !tipoComprobanteId || !fechaAsiento || !documentoRespaldo) {
            alert("Todos los campos son obligatorios.");
            return;
        }

        const today = new Date().toISOString().split('T')[0];
        $('#fecha_asiento').attr('max', today);
        if (fechaAsiento > today) {
            alert('La fecha del asiento no puede ser posterior al día de hoy.');
            return;
        }

        const formData = new FormData();
        formData.append('num_asiento', numAsiento);
        formData.append('tipo_comprobante', tipoComprobanteId);
        formData.append('fecha', fechaAsiento);
        formData.append('documento_respaldo', documentoRespaldo);

        $.ajax({
            url: 'http://localhost:9000/asientos',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                alert('Asiento creado con éxito');
                cargarAsientosContables();  // Recargar la lista de asientos
            },
            error: function (error) {
                console.error('Error al crear el asiento:', error);
                alert('Hubo un problema al crear el asiento.');
            }
        });
    });

    // Manejar la visualización de un asiento seleccionado
    $('#lista_asientos_contables').on('click', '.ver-asiento-btn', function () {
        // Obtener el ID del asiento desde el botón que fue clicado
        const asientoId = $(this).data('id');
        
        // Verificar que el ID del asiento sea válido
        if (!asientoId) {
            alert("Selecciona un asiento contable.");
            return;
        }

        // Realizar la solicitud GET para obtener los detalles del asiento seleccionado
        $.ajax({
            url: `http://localhost:9000/asientos/${asientoId}`,  // Aquí se construye la URL con el ID del asiento
            method: 'GET',  // Método HTTP GET para obtener los datos
            success: function (response) {
                // Si la solicitud tiene éxito, mostrar los detalles del asiento
                mostrarDetalleAsiento(response);
            },
            error: function (error) {
                // Si ocurre un error, mostrar un mensaje en la consola y un alerta al usuario
                console.error('Error al cargar el asiento:', error);
                alert('Hubo un problema al cargar el asiento.');
            }
        });
    });


    // Manejar la adición de cuentas a un asiento
    $('#agregar_cuenta_btn').click(function () {
        const asientoId = $('#detalle_asiento').data('asiento-id');
        const cuentaId = $('#cuenta_contable').val();
        const debeHaber = $('#debe_haber').val();
        const monto = $('#monto').val();

        if (!cuentaId || !debeHaber || !monto) {
            alert("Todos los campos son obligatorios.");
            return;
        }

        $.ajax({
            url: `http://localhost:9000/asientos/${asientoId}/cuentas`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                cuentaId: cuentaId,
                debe_haber: debeHaber,
                monto: monto
            }),
            success: function (response) {
                alert('Cuenta agregada con éxito');
                mostrarDetalleAsiento(response);  // Recargar el detalle del asiento
            },
            error: function (error) {
                console.error('Error al agregar la cuenta:', error);
                alert('Hubo un problema al agregar la cuenta.');
            }
        });
    });

    // Funciones auxiliares
    function cargarTiposDeComprobante() {
        $.ajax({
            url: 'http://localhost:9000/tipo_comprobante',
            method: 'GET',
            success: function (response) {
                const tipoComprobanteSelect = $('#tipo_comprobante');
                tipoComprobanteSelect.empty();
                response.forEach(tipo => {
                    tipoComprobanteSelect.append(`<option value="${tipo.id_tipo_comprobante}">${tipo.nombre_comprobante}</option>`);
                });
            },
            error: function (error) {
                console.error('Error al cargar tipos de comprobante:', error);
            }
        });
    }

    function cargarAsientosContables() {
        $.ajax({
            url: 'http://localhost:9000/asientos',
            method: 'GET',
            success: function (response) {
                const listaAsientos = $('#lista_asientos_contables');
                listaAsientos.empty();
                response.forEach(asiento => {
                    const li = $(`
                        <li>
                            Asiento N° ${asiento.num_asiento} - ${asiento.fecha}
                            <button class="ver-asiento-btn" data-id="${asiento.id_asiento_contable}">Ver Asiento</button>
                        </li>
                    `);
                    listaAsientos.append(li);
                });
            },
            error: function (error) {
                console.error('Error al cargar los asientos contables:', error);
            }
        });
    }

    function mostrarDetalleAsiento(asiento) {
        $('#detalle_num_asiento').text(`Número de Asiento: ${asiento.num_asiento}`);
        $('#detalle_tipo_comprobante').text(`Tipo de Comprobante: ${asiento.tipo_comprobante.nombre_comprobante}`);
        $('#detalle_fecha_asiento').text(`Fecha del Asiento: ${asiento.fecha}`);
        $('#detalle_asiento').data('asiento-id', asiento.id_asiento_contable).show();

        const listaCuentas = $('#lista_cuentas');
        listaCuentas.empty();
        asiento.cuentas.forEach(cuenta => {
            listaCuentas.append(`<li>${cuenta.nombre_cuenta} - ${cuenta.debe_haber} - ${cuenta.monto}</li>`);
        });
    }
});
