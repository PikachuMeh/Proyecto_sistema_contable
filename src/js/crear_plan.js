$(function () {
    const empresaSeleccionada = JSON.parse(localStorage.getItem('empresaSeleccionada'));
    if (empresaSeleccionada && empresaSeleccionada.id) {
        $("#empresa-nombre").text(empresaSeleccionada.nombre);
    } else {
        alert("No se ha seleccionado una empresa válida.");
        return;
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
            fecha: $("#fecha").val(),
            estado: "abierto",
            documento_respaldo: $("#documento-respaldo").val()
        };
        
        if (!validarCuenta(cuenta)) {
            return;
        }

        cuentas.push(cuenta);
        updateCuentasList();
        clearForm();
    });

    function validarCuenta(cuenta) {
        // Validar campos vacíos
        if (!cuenta.codigo_cuenta || !cuenta.descripcion_cuenta || !cuenta.nombre_cuenta || !cuenta.nivel_cuenta || !cuenta.tipo_cuenta || !cuenta.saldo_normal) {
            alert("Todos los campos son obligatorios, excepto el estado.");
            return false;
        }

        // Validar código de cuenta único
        if (cuentas.some(c => c.codigo_cuenta === cuenta.codigo_cuenta)) {
            alert("El código de cuenta ya existe.");
            return false;
        }

        // Validar nombre de cuenta único
        if (cuentas.some(c => c.nombre_cuenta === cuenta.nombre_cuenta)) {
            alert("El nombre de la cuenta ya existe.");
            return false;
        }

        // Validar jerarquía de código de cuenta
        const codigoPartes = cuenta.codigo_cuenta.split('.');
        let esValido = true;
        if (codigoPartes.length > 1) {
            let codigoPadre = codigoPartes.slice(0, -1).join('.');
            esValido = cuentas.some(c => c.codigo_cuenta === codigoPadre);
        } else {
            // Verificar si es un número y si ya existe
            if (isNaN(cuenta.codigo_cuenta) || cuentas.some(c => c.codigo_cuenta === cuenta.codigo_cuenta)) {
                alert("Debe existir una cuenta principal antes de crear una subcuenta.");
                return false;
            }
        }

        if (!esValido) {
            alert("Debe existir una cuenta padre para crear una subcuenta.");
            return false;
        }

        return true;
    }

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
        $("#documento-respaldo").val('');
    }

    $("#crear-plan-btn").click(function () {
        if (cuentas.length === 0) {
            alert("No hay cuentas agregadas.");
            return;
        }

        $.ajax({
            url: `http://localhost:9000/empresas/${empresaSeleccionada.id}/crear-cuentas-y-plan`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(cuentas),  // Enviar solo las cuentas como una lista
            success: function (response) {
                alert("Plan de cuentas y asientos contables creados con éxito.");
                window.location.href = 'empresas.html';
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });
});
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

    // Aquí puedes manejar el evento de agregar cuenta al plan (si se crea desde cero)
    $('#add-cuenta-btn').click(function() {
        // Código para agregar cuenta
    });

    // Aquí puedes manejar la subida del archivo Excel
    $('#upload-plan-btn').click(function() {
        const archivo = $('#archivo-excel')[0].files[0];
        if (archivo) {
            const formData = new FormData();
            formData.append('archivo', archivo);

            $.ajax({
                url: 'ruta_a_tu_api_para_subir_el_excel', // Cambia a la ruta de tu API
                method: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    alert('Plan de cuentas subido con éxito');
                },
                error: function(error) {
                    console.error('Error al subir el archivo:', error);
                }
            });
        } else {
            alert('Por favor, selecciona un archivo');
        }
    });
});
