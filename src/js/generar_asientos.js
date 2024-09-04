$(document).ready(function () {
    // Establecer la fecha máxima en el campo de fecha al día de hoy
    const today = new Date().toISOString().split('T')[0];
    $('#fecha_asiento').attr('max', today);

    let empresaSeleccionada = JSON.parse(localStorage.getItem('empresaSeleccionada'));
    let empresaId = empresaSeleccionada ? empresaSeleccionada.id : null;
    cargarTiposDeComprobante();
    cargarAsientosContables(empresaId);
    
    if (!empresaId) {
        alert("No se ha seleccionado ninguna empresa.");
        return;
    }

    // Manejar la creación de un nuevo asiento contable
    $('#crear_asiento_btn').click(function () {
        const numAsiento = $('#num_asiento').val();
        const tipoComprobanteId = $('#tipo_comprobante').val();
        const fechaAsiento = $('#fecha_asiento').val();
        const documentoRespaldo = $('#documento_respaldo')[0].files[0];

        // Validación específica para la creación de un asiento
        if (!numAsiento || !tipoComprobanteId || !fechaAsiento || !documentoRespaldo) {
            alert("Todos los campos son obligatorios para crear un asiento.");
            return;
        }

        // Validar que la fecha del asiento no sea posterior al día de hoy
        if (fechaAsiento > today) {
            alert('La fecha del asiento no puede ser posterior al día de hoy.');
            return;
        }

        $.ajax({
            url: `http://localhost:9000/asientos/verificar/${empresaId}/${numAsiento}`,
            method: 'GET',
            success: function (response) {
                if (response.exists) {
                    alert('El número de asiento ya existe para esta empresa.');
                } else {
                    const formData = new FormData();
                    formData.append('num_asiento', numAsiento);
                    formData.append('tipo_comprobante', tipoComprobanteId);
                    formData.append('fecha', fechaAsiento);
                    formData.append('documento_respaldo', documentoRespaldo);
                    formData.append('empresa_id', empresaId);
                    
                    $.ajax({
                        url: 'http://localhost:9000/asientos',
                        method: 'POST',
                        data: formData,
                        contentType: false,
                        processData: false,
                        success: function (response) {
                            alert('Asiento creado con éxito');
                            cargarAsientosContables(empresaId);
                        },
                        error: function (error) {
                            console.error('Error al crear el asiento:', error);
                            alert('Hubo un problema al crear el asiento.');
                        }
                    });
                }
            },
            error: function (xhr, status, error) {
                console.error('Error al verificar el número de asiento:', xhr.responseText || error);
                alert(`Error al verificar el número de asiento: ${xhr.status} ${xhr.statusText}`);
            }
        });
    });

    // Manejar la adición de cuentas al asiento existente
    $('#agregar_cuenta_btn').click(function () {
        const asientoId = $('#detalle_asiento').data('asiento-id');
        const cuentaId = $('#cuenta_contable').val();
        const debeHaber = $('#debe_haber').val();
        const monto = $('#monto').val();

        // Validación específica para agregar una cuenta
        if (!cuentaId || !debeHaber || !monto) {
            alert("Todos los campos son obligatorios para agregar una cuenta.");
            return;
        }

        $.ajax({
            url: `http://localhost:9000/asientos/${asientoId}/cuentas`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                cuentaId: parseInt(cuentaId),
                debe_haber: debeHaber,
                monto: parseFloat(monto)
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
    $('#lista_asientos_contables').on('click', '.ver-asiento-btn', function () {
        const asientoId = $(this).data('id');
        
        if (!asientoId) {
            alert("Selecciona un asiento contable.");
            return;
        }
        
        // Guardar el ID del asiento seleccionado en localStorage
        localStorage.setItem('asientoSeleccionado', asientoId);
        
        // Redirigir a la página de detalle del asiento
        window.location.href = `cuentas_asientos.html?asiento_id=${asientoId}`;
    });
    
    // Otras funciones
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

    function cargarAsientosContables(empresaId) {
        $.ajax({
            url: `http://localhost:9000/asientos/${empresaId}`,
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
                alert(error['responseJSON']['detail'])
                console.error('Error al cargar los asientos contables:', error);
            }
        });
    }
    

    function mostrarDetalleAsiento(asiento) {
        $('#detalle_num_asiento').text(`Número de Asiento: ${asiento.num_asiento}`);
        $('#detalle_tipo_comprobante').text(`Tipo de Comprobante: ${asiento.tipo_comprobante}`);
        $('#detalle_fecha_asiento').text(`Fecha del Asiento: ${asiento.fecha}`);
        $('#detalle_asiento').data('asiento-id', asiento.id_asiento_contable).show();

        
    }
});
