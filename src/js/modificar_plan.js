$(document).ready(function () {
    const planId = localStorage.getItem('planIdSeleccionado');
    const empresaId = localStorage.getItem('empresaIdSeleccionada');

    if (!planId || !empresaId) {
        alert("No se ha seleccionado ningún plan de cuentas.");
        window.location.href = "empresas.html";
        return;
    }

    // Cargar la información del plan de cuentas
    cargarPlanDeCuentas(empresaId, planId);

    function cargarPlanDeCuentas(empresaId, planId) {
        $.ajax({
            url: `http://localhost:9000/empresas/${empresaId}/planes/${planId}/cuentas`,
            method: 'GET',
            contentType: 'application/json',
            success: function (response) {
                console.log('Respuesta de la API:', response);
                displayCuentasContables(response);
            },
            error: function (error) {
                console.error('Error al cargar el plan de cuentas:', error);
                alert('Hubo un error al cargar el plan de cuentas.');
                window.location.href = "empresas.html";
            }
        });
    }

    function displayCuentasContables(cuentas) {
        const cuentasPrincipalesDiv = $("#lista-cuentas-principales");
        const cuentasNormalesDiv = $("#lista-cuentas-normales");
        cuentasPrincipalesDiv.empty();
        cuentasNormalesDiv.empty();

        if (cuentas.length === 0) {
            cuentasNormalesDiv.append('<p>No se encontraron cuentas contables para este plan.</p>');
            return;
        }

        const cuentasPrincipales = [];
        const cuentasNormales = [];

        cuentas.forEach(cuenta => {
            const cuentaDiv = $(`
                <div class="cuenta-div" data-id="${cuenta.id_cuenta_contable}">
                    <input type="checkbox" class="principal-checkbox" data-id="${cuenta.id_cuenta_contable}" ${cuenta.es_principal ? 'checked' : ''}>
                    <label><strong>${cuenta.codigo}:</strong> ${cuenta.nombre_cuenta} (Saldo: ${cuenta.saldo_normal})</label>
                </div>
            `);
            if (cuenta.es_principal) {
                cuentasPrincipales.push({ codigo: cuenta.codigo, element: cuentaDiv });
            } else {
                cuentasNormales.push({ codigo: cuenta.codigo, element: cuentaDiv });
            }
        });

        // Ordenar y añadir las cuentas al DOM
        cuentasPrincipales.sort((a, b) => a.codigo.localeCompare(b.codigo));
        cuentasNormales.sort((a, b) => a.codigo.localeCompare(b.codigo));
        cuentasPrincipales.forEach(cuenta => cuentasPrincipalesDiv.append(cuenta.element));
        cuentasNormales.forEach(cuenta => cuentasNormalesDiv.append(cuenta.element));
    }

    // Manejar el cambio de la selección de cuentas principales
    $("#cuentas-principales, #cuentas-contables").on('change', '.principal-checkbox', function () {
        const cuentaId = $(this).data('id');
        const esPrincipal = $(this).is(':checked');
        const cuentaDiv = $(this).closest('.cuenta-div');

        $.ajax({
            url: `http://localhost:9000/cuentas/${cuentaId}/actualizar-principal`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ es_principal: esPrincipal }),
            success: function () {
                if (esPrincipal) {
                    $("#lista-cuentas-principales").append(cuentaDiv);
                } else {
                    $("#lista-cuentas-normales").append(cuentaDiv);
                }
                ordenarCuentas();
            },
            error: function (error) {
                console.error('Error al actualizar la cuenta contable:', error);
                alert('Hubo un error al actualizar la cuenta contable.');
            }
        });
    });

    function ordenarCuentas() {
        const cuentasPrincipalesDiv = $("#lista-cuentas-principales");
        const cuentasNormalesDiv = $("#lista-cuentas-normales");

        const cuentasPrincipales = cuentasPrincipalesDiv.children(".cuenta-div").get();
        cuentasPrincipales.sort((a, b) => $(a).find('label').text().localeCompare($(b).find('label').text()));
        cuentasPrincipalesDiv.append(cuentasPrincipales);

        const cuentasNormales = cuentasNormalesDiv.children(".cuenta-div").get();
        cuentasNormales.sort((a, b) => $(a).find('label').text().localeCompare($(b).find('label').text()));
        cuentasNormalesDiv.append(cuentasNormales);
    }

    // Mostrar el modal para agregar nueva cuenta
    $("#open-modal-btn").click(function () {
        $("#add-account-modal").show();
    });

    // Ocultar el modal
    $("#close-modal-btn").click(function () {
        $("#add-account-modal").hide();
    });

    // Validar y manejar el envío del formulario para agregar una nueva cuenta
    $("#agregar_cuenta").submit(function (event) {
        event.preventDefault();

        const codigo = $("#codigo").val().trim();
        const descripcion = $("#descripcion").val().trim();
        const saldo = parseFloat($("#saldo").val());

        // Validación para el código de cuenta (solo números y puntos)
        const codigoValido = /^[\d.]+$/.test(codigo);
        if (!codigoValido) {
            alert("El código de cuenta solo puede contener números y puntos.");
            return;
        }

        // Validación para la descripción (sin caracteres especiales)
        const descripcionValida = /^[a-zA-Z\s]+$/.test(descripcion);
        if (!descripcionValida) {
            alert("La descripción solo puede contener letras y espacios.");
            return;
        }

        // Validación para el saldo (no negativo)
        if (isNaN(saldo) || saldo < 0) {
            alert("El saldo debe ser un número positivo.");
            return;
        }

        // Validar que el código no exista ya
        const existeCodigo = $(".cuenta-div").filter(function () {
            return $(this).find('label').text().startsWith(`${codigo}:`);
        }).length > 0;

        if (existeCodigo) {
            alert("El código de cuenta ya existe.");
            return;
        }

        // Enviar la solicitud AJAX para agregar la nueva cuenta
        $.ajax({
            url: `http://localhost:9000/empresas/${empresaId}/planes/${planId}/cuentas`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ codigo, descripcion, saldo }),
            success: function () {
                alert('Cuenta agregada con éxito.');
                $("#add-account-modal").hide();
                cargarPlanDeCuentas(empresaId, planId);  // Recargar las cuentas
            },
            error: function (error) {
                console.error('Error al agregar la cuenta:', error);
                alert('Hubo un error al agregar la cuenta.');
                console.log('Detalles del error:', error.responseText);  // Agrega esta línea
            }
            
        });
    });
});
