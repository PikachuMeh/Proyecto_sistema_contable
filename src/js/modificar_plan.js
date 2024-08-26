$(document).ready(function () {
    const params = new URLSearchParams(window.location.search);
    const planId = params.get('planId');
    const empresaId = params.get('empresaId');

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
        const cuentasDiv = $("#cuentas-contables");
        cuentasDiv.empty();

        cuentas.forEach(cuenta => {
            const cuentaDiv = $(`
                <div>
                    <input type="checkbox" class="principal-checkbox" data-id="${cuenta.id_cuenta_contable}" ${cuenta.es_principal ? 'checked' : ''}>
                    <label><strong>${cuenta.codigo}:</strong> ${cuenta.nombre_cuenta} (Saldo: ${cuenta.saldo_normal})</label>
                </div>
            `);
            cuentasDiv.append(cuentaDiv);
        });
    }

    // Manejar el cambio de la selección de cuentas principales
    $("#cuentas-contables").on('change', '.principal-checkbox', function () {
        const cuentaId = $(this).data('id');
        const esPrincipal = $(this).is(':checked');

        // Actualizar la cuenta contable en el servidor
        $.ajax({
            url: `http://localhost:9000/cuentas/${cuentaId}/actualizar-principal`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ es_principal: esPrincipal }),
            success: function (response) {
                console.log('Cuenta contable actualizada con éxito:', response);
            },
            error: function (error) {
                console.error('Error al actualizar la cuenta contable:', error);
                alert('Hubo un error al actualizar la cuenta contable.');
            }
        });
    });
});