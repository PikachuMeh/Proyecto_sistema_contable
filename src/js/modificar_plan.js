$(document).ready(function() {
    const empresaSeleccionada = JSON.parse(localStorage.getItem('empresaSeleccionada'));
    const planSeleccionado = JSON.parse(localStorage.getItem('planSeleccionado'));

    if (empresaSeleccionada && planSeleccionado) {
        cargarCuentas(planSeleccionado.id_plan_cuentas);
    } else {
        alert('No se seleccionó un plan de cuentas válido.');
    }

    function cargarCuentas(idPlanCuentas) {
        $.ajax({
            url: `http://localhost:9000/planes/${idPlanCuentas}/cuentas`,
            method: 'GET',
            contentType: 'application/json',
            success: function(response) {
                mostrarCuentas(response);
            },
            error: function(error) {
                console.error('Error al cargar las cuentas:', error);
            }
        });
    }

    function mostrarCuentas(cuentas) {
        const cuentasPrincipalesDiv = $("#cuentas-principales");
        const cuentasNormalesDiv = $("#cuentas-normales");

        cuentasPrincipalesDiv.empty();
        cuentasNormalesDiv.empty();

        cuentasPrincipalesDiv.append("<h2>Cuentas Principales</h2>");
        cuentasNormalesDiv.append("<h2>Cuentas Normales</h2>");

        cuentas.forEach(cuenta => {
            const cuentaDiv = $(`
                <div>
                    <p><strong>Código:</strong> ${cuenta.codigo}</p>
                    <p><strong>Descripción:</strong> ${cuenta.descripcion}</p>
                    <p><strong>Saldo:</strong> ${cuenta.saldo_normal}</p>
                </div>
            `);

            if (cuenta.tipo_cuenta === 'Principal') {
                cuentasPrincipalesDiv.append(cuentaDiv);
            } else {
                cuentasNormalesDiv.append(cuentaDiv);
            }
        });
    }
});
