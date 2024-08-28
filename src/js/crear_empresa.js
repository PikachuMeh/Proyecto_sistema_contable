$(document).ready(function () {
    $("#crear-empresa-form").submit(function (event) {
        event.preventDefault();

        const nombre = $("#nombre").val().trim();
        const fecha_constitucion = $("#fecha_constitucion").val().trim();
        const rif = $("#rif").val().trim();
        const fecha_ejercicio_economico = $("#fecha_ejercicio_economico").val().trim();
        const fecha_contable = $("#fecha_contable").val().trim();
        const actividad_economica = $("#actividad_economica").val().trim();
        const direccion = $("#direccion").val().trim();
        const correo = $("#correo").val().trim();

        if (!nombre || !fecha_constitucion || !rif || !fecha_ejercicio_economico || !fecha_contable || !actividad_economica || !direccion || !correo) {
            $("#mensaje").text("Todos los campos son obligatorios.");
            return;
        }

        // Enviar los datos a la API
        $.ajax({
            url: 'http://localhost:9000/empresas/crear',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 
                nombre, 
                fecha_constitucion, 
                rif, 
                fecha_ejercicio_economico, 
                fecha_contable, 
                actividad_economica, 
                direccion, 
                correo 
            }),
            success: function (response) {
                $("#mensaje").text("Empresa creada con éxito.");
                $("#crear-empresa-form")[0].reset();
            },
            error: function (error) {
                console.error('Error al crear la empresa:', error);
                $("#mensaje").text("Hubo un error al crear la empresa. Inténtalo de nuevo.");
            }
        });
    });

    $("#volver-btn").click(function () {
        window.location.href = 'empresas.html';
    });
});
