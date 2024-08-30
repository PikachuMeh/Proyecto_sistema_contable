$(document).ready(function () {
    const empresaId = localStorage.getItem('empresaIdSeleccionada');
    const planId = localStorage.getItem('planIdSeleccionado');
    let asientoId = null;

    if (!empresaId || !planId) {
        alert("No se ha seleccionado una empresa o un plan de cuentas.");
        window.location.href = 'empresas.html';
        return;
    }

    // Cargar las cuentas disponibles
    cargarCuentasDisponibles();

    function cargarCuentasDisponibles() {
        $.ajax({
            url: `http://localhost:9000/empresas/${empresaId}/planes/${planId}/cuentas`,
            method: 'GET',
            contentType: 'application/json',
            success: function (response) {
                displayCuentasDisponibles(response);
            },
            error: function (error) {
                console.error('Error al cargar las cuentas:', error);
            }
        });
    }

    function displayCuentasDisponibles(cuentas) {
        const cuentasDiv = $("#cuentas-disponibles");
        cuentasDiv.empty();
        cuentas.forEach(cuenta => {
            const cuentaDiv = $(`
                <div>
                    <input type="checkbox" class="cuenta-checkbox" data-id="${cuenta.id_cuenta_contable}">
                    <label>${cuenta.codigo} - ${cuenta.nombre_cuenta} (Saldo: ${cuenta.saldo_normal})</label>
                </div>
            `);
            cuentasDiv.append(cuentaDiv);
        });
    }

    // Crear un nuevo asiento contable
    $("#crear-asiento-btn").click(function () {
        $.ajax({
            url: `http://localhost:9000/empresas/${empresaId}/asientos`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ planId: planId }),
            success: function (response) {
                asientoId = response.asiento_id;
                $("#asiento-activo").show();
                alert("Asiento contable creado con éxito. Puedes agregar cuentas.");
            },
            error: function (error) {
                console.error('Error al crear el asiento contable:', error);
                alert('Hubo un error al crear el asiento contable.');
            }
        });
    });

    // Añadir cuentas al asiento contable
    $("#cuentas-disponibles").on('change', '.cuenta-checkbox', function () {
        const cuentaId = $(this).data('id');
        const checked = $(this).is(':checked');
        
        if (asientoId) {
            $.ajax({
                url: `http://localhost:9000/asientos/${asientoId}/cuentas`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ cuentaId: cuentaId, checked: checked }),
                success: function (response) {
                    updateAsientoView(response);
                },
                error: function (error) {
                    console.error('Error al actualizar el asiento contable:', error);
                    alert('Hubo un error al actualizar el asiento contable.');
                }
            });
        } else {
            alert('Primero debes crear un asiento contable.');
            $(this).prop('checked', false);
        }
    });

    // Cerrar el asiento contable
    $("#cerrar-asiento-btn").click(function () {
        if (asientoId) {
            $.ajax({
                url: `http://localhost:9000/asientos/${asientoId}/cerrar`,
                method: 'POST',
                contentType: 'application/json',
                success: function () {
                    alert('Asiento contable cerrado con éxito.');
                    $("#asiento-activo").hide();
                    asientoId = null;
                },
                error: function (error) {
                    console.error('Error al cerrar el asiento contable:', error);
                    alert('No se puede cerrar el asiento porque no cuadra.');
                }
            });
        }
    });

    function updateAsientoView(cuentas) {
        const cuentasSeleccionadasDiv = $("#cuentas-seleccionadas");
        cuentasSeleccionadasDiv.empty();
        cuentas.forEach(cuenta => {
            const cuentaDiv = $(`
                <div>
                    <span>${cuenta.codigo} - ${cuenta.nombre_cuenta} (Debe: ${cuenta.debe}, Haber: ${cuenta.haber})</span>
                </div>
            `);
            cuentasSeleccionadasDiv.append(cuentaDiv);
        });
    }
});
