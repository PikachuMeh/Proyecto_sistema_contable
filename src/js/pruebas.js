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
            const empresaDiv = $(`
                <div>
                    <span>${empresa.nombre}</span>
                    <button class="select-btn" data-id="${empresa.id_empresas}" data-nombre="${empresa.nombre}">Seleccionar</button>
                </div>
            `);
            resultsDiv.append(empresaDiv);
        });

        $(".select-btn").click(function () {
            const empresaId = $(this).data('id');
            const empresaNombre = $(this).data('nombre');
            localStorage.setItem('empresaSeleccionada', JSON.stringify({ id: empresaId, nombre: empresaNombre }));

            $.ajax({
                url: `http://localhost:9000/empresas/${empresaId}/planes`,
                method: 'POST',
                contentType: 'application/json',
                success: function (response) {
                    if (response.length > 0) {
                        displayPlanesDeCuentas(response); // Mostrar los planes de cuentas existentes
                    } else {
                        showCreatePlanButton(); // Mostrar el botón para crear un nuevo plan
                    }
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        });
    }

    function displayPlanesDeCuentas(planes) {
        const planesDiv = $("#planes-de-cuentas");
        planesDiv.empty();
        planes.forEach(plan => {
            const planDiv = $(`
                <div>
                    <p><strong>Código:</strong> ${plan.codigo}</p>
                    <p><strong>Descripción:</strong> ${plan.descripcion_cuenta}</p>
                    <p><strong>Estado:</strong> ${plan.estado}</p>
                    <!-- Agrega más detalles del plan de cuentas según sea necesario -->
                </div>
            `);
            planesDiv.append(planDiv);
        });
    }

    function showCreatePlanButton() {
        const createButton = $("<button>Crear nuevo plan de cuentas</button>");
        createButton.click(function () {
            window.location.href = 'crear_plan.html';
        });
        $("#planes-de-cuentas").empty().append(createButton);
    }
});
