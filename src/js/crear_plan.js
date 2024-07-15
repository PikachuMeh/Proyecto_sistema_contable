$(function () {
    const empresaSeleccionada = JSON.parse(localStorage.getItem('empresaSeleccionada'));
    if (empresaSeleccionada) {
        $("#empresa-nombre").text(empresaSeleccionada.nombre);
    }

    let cuentas = [];

    $("#add-cuenta-btn").click(function () {
        const cuenta = {
            codigo_cuenta: $("#codigo-cuenta").val(),
            descripcion_cuenta: $("#descripcion-cuenta").val(),
            nombre_cuenta: $("#nombre-cuenta").val(),
            nivel_cuenta: $("#nivel-cuenta").val(),
            tipo_cuenta: $("#tipo-cuenta").val(),
            saldo_normal: $("#saldo-normal").val(),
            estado: "abierto"
        };

        // Validar que el código de cuenta no se repita
        if (cuentas.some(c => c.codigo_cuenta === cuenta.codigo_cuenta)) {
            alert("El código de cuenta ya existe.");
            return;
        }

        // Validar que el nombre de la cuenta no se repita
        if (cuentas.some(c => c.nombre_cuenta === cuenta.nombre_cuenta)) {
            alert("El nombre de la cuenta ya existe.");
            return;
        }

        cuentas.push(cuenta);
        updateCuentasList();
        clearForm();
    });

    function updateCuentasList() {
        const cuentasList = $("#cuentas-list");
        cuentasList.empty();
        cuentas.forEach(cuenta => {
            const cuentaItem = $(`<li>${cuenta.codigo_cuenta} - ${cuenta.nombre_cuenta} - ${cuenta.descripcion_cuenta}</li>`);
            cuentasList.append(cuentaItem);
        });
    }

    function clearForm() {
        $("#codigo-cuenta").val('');
        $("#descripcion-cuenta").val('');
        $("#nombre-cuenta").val('');
        $("#nivel-cuenta").val('');
        $("#tipo-cuenta").val('');
        $("#saldo-normal").val('');
    }

    $("#crear-plan-btn").click(function () {
        if (cuentas.length === 0) {
            alert("No hay cuentas agregadas.");
            return;
        }

        $.ajax({
            url: `http://localhost:9000/empresas/${empresaSeleccionada.id}/crear-plan`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(cuentas),
            success: function (response) {
                alert("Plan de cuentas creado con éxito.");
                window.location.href = 'index.html';  // Cambia 'index.html' al archivo correcto
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });
});
