$(document).ready(function() {
    $("#crear-plan-form").submit(function(event) {
        event.preventDefault();

        const codigoCuenta = $("#codigo_cuenta").val().trim();
        const descripcionCuenta = $("#descripcion_cuenta").val().trim();
        const nombreCuenta = $("#nombre_cuenta").val().trim();
        const nivelCuenta = $("#nivel_cuenta").val().trim();
        const tipoCuenta = $("#tipo_cuenta").val().trim();
        const saldoNormal = $("#saldo_normal").val().trim();

        if (!codigoCuenta || !descripcionCuenta || !nombreCuenta || !nivelCuenta || !tipoCuenta || !saldoNormal) {
            alert("Todos los campos son requeridos.");
            return;
        }

        // Mostrar el resumen de la cuenta
        const cuentaResumen = `
            <h2>Resumen de la Cuenta</h2>
            <p><strong>Código de Cuenta:</strong> ${codigoCuenta}</p>
            <p><strong>Descripción de la Cuenta:</strong> ${descripcionCuenta}</p>
            <p><strong>Nombre de la Cuenta:</strong> ${nombreCuenta}</p>
            <p><strong>Nivel de la Cuenta:</strong> ${nivelCuenta}</p>
            <p><strong>Tipo de Cuenta:</strong> ${tipoCuenta}</p>
            <p><strong>Saldo Normal:</strong> ${saldoNormal}</p>
            <button id="confirmar-creacion">Confirmar Creación</button>
        `;
        $("#cuenta-resumen").html(cuentaResumen);

        // Manejar la confirmación de creación
        $("#confirmar-creacion").click(function() {
            const cuentaData = {
                codigo_cuenta: codigoCuenta,
                descripcion_cuenta: descripcionCuenta,
                nombre_cuenta: nombreCuenta,
                nivel_cuenta: nivelCuenta,
                tipo_cuenta: tipoCuenta,
                saldo_normal: saldoNormal,
                estado: 'abierto'
            };

            $.ajax({
                url: 'http://localhost:9000/crear-plan-cuenta',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(cuentaData),
                success: function(response) {
                    alert('Cuenta creada con éxito');
                    // Redirigir o limpiar formulario después de la creación exitosa
                    $("#crear-plan-form")[0].reset();
                    $("#cuenta-resumen").empty();
                },
                error: function(error) {
                    console.error('Error:', error);
                    alert('Hubo un error al crear la cuenta.');
                }
            });
        });
    });
});
