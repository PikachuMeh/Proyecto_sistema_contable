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
                    if (response.message) {
                        alert(response.message);
                        showCreatePlanButton();
                    } else {
                        displayPlanesDeCuentas(response);
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
        if (planes.length === 0) {
            planesDiv.append("<p>No se encontraron planes de cuentas.</p>");
            showCreatePlanButton();
        } else {
            planes.forEach(plan => {
                const planDiv = $(`<div>${plan.descripcion_cuenta}</div>`);
                planesDiv.append(planDiv);
            });
        }
    }

    function showCreatePlanButton() {
        const createButton = $("<button>Crear nuevo plan de cuentas</button>");
        createButton.click(function () {
            window.location.href = 'crear_plan.html';
        });
        $("#planes-de-cuentas").append(createButton);
    }
});
