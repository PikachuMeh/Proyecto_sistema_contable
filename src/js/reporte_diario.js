$(function () {
    $("#search-btn").click(function () {
        const query = $("#empresa-search").val();
        $.ajax({
            url: 'http://localhost:9000/buscar-empresas',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: query }),
            success: function (response) {
                displaySearchResults(response);
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

    function displaySearchResults(empresas) {
        const resultsDiv = $("#search-results");
        resultsDiv.empty();
        empresas.forEach(empresa => {
            console.log("Datos de la empresa:", empresa); // Verifica todos los datos de la empresa recibidos
            const empresaDiv = $(`
                <div>
                    <span>${empresa.nombre}</span>
                    <button class="select-btn" data-id="${empresa.id_empresas}" data-nombre="${empresa.nombre}">Seleccionar</button>
                </div>
            `);
            resultsDiv.append(empresaDiv);
        });
    }

    // Delegación de eventos para manejar clic en botones .select-btn
    $(document).on('click', '.select-btn', function () {
        const empresaId = $(this).data('id');
        const empresaNombre = $(this).data('nombre');
        console.log("ID de la empresa seleccionada:", empresaId); // Verifica que capture el ID correctamente
        localStorage.setItem('empresaSeleccionada', JSON.stringify({ id: empresaId, nombre: empresaNombre }));
        // Resto del código AJAX para obtener o crear planes de cuentas
    
        mostrarFormularioReporte(empresaId, empresaNombre);
    });

    function mostrarFormularioReporte(empresaId, empresaNombre) {
        const formDiv = $("#report-form");
        formDiv.empty();
        const formHtml = `
            <h3>Crear Reporte para ${empresaNombre}</h3>
            <form id="crear-reporte-form">
                <label for="fecha-inicio">Fecha de Inicio:</label>
                <input type="date" id="fecha-inicio" name="fecha-inicio" required><br>
                <label for="fecha-fin">Fecha de Fin:</label>
                <input type="date" id="fecha-fin" name="fecha-fin" required><br>
                <label for="nivel-detalle">Nivel de Detalle:</label>
                <input type="text" id="nivel-detalle" name="nivel-detalle" required><br>
                <label for="formato">Formato:</label>
                <input type="text" id="formato" name="formato" required><br>
                <button type="submit">Crear Reporte</button>
            </form>
        `;
        formDiv.append(formHtml);

        $("#crear-reporte-form").submit(function (e) {
            e.preventDefault();
            const fechaInicio = $("#fecha-inicio").val();
            const fechaFin = $("#fecha-fin").val();
            const nivelDetalle = $("#nivel-detalle").val();
            const formato = $("#formato").val();

            $.ajax({
                url: `http://localhost:9000/empresas/${empresaId}/crear-reporte`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    fecha_inicio: fechaInicio,
                    fecha_fin: fechaFin,
                    nivel_detalle: nivelDetalle,
                    formato: formato
                }),
                success: function (response) {
                    alert(response.message);
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        });
    }
});
