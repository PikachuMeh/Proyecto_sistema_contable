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

    // Delegación de eventos para manejar clic en botones .select-btn
    $("#search-results").on('click', '.select-btn', function () {
        const empresaId = $(this).data('id');
        const empresaNombre = $(this).data('nombre');
        console.log("ID de la empresa seleccionada:", empresaId);
    
        // Guarda la empresa seleccionada en localStorage
        localStorage.setItem('empresaSeleccionada', JSON.stringify({ id: empresaId, nombre: empresaNombre }));
    
        // Llama a la función para obtener los planes de cuentas
        obtenerPlanesCuentas(empresaId);
    });

    function obtenerPlanesCuentas(empresaId) {
        // Limpiar el contenedor de planes de cuentas y el botón de generar asientos contables
        $("#planes-de-cuentas").empty();
        $("#asientos-contables-container").empty();
    
        $.ajax({
            url: `http://localhost:9000/empresas/${empresaId}/planes`,
            method: 'GET',
            contentType: 'application/json',
            success: function (response) {
                if (response.length > 0) {
                    // Verifica si hay cuentas contables para el primer plan de cuentas encontrado
                    verificarCuentasContables(response[0].id_plan_cuentas, empresaId, response);
                } else {
                    showCreatePlanButton();
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    }

    function verificarCuentasContables(planId, empresaId, planes) {
        $.ajax({
            url: `http://localhost:9000/empresas/${empresaId}/planes/${planId}/cuentas`,
            method: 'GET',
            contentType: 'application/json',
            success: function (response) {
                if (response.length > 0) {
                    displayPlanesDeCuentas(planes, empresaId);
                    showGenerarAsientosButton();
                } else {
                    displayPlanesDeCuentas(planes, empresaId);
                }
            },
            error: function (error) {
                console.error('Error al verificar las cuentas contables:', error);
            }
        });
    }

    function displayPlanesDeCuentas(planes, empresaId) {
        const planesDiv = $("#planes-de-cuentas");
        planesDiv.empty();

        planes.forEach(plan => {
            const planDiv = $(`
                <div>
                    <p><strong>Código:</strong> ${plan.codigo}</p>
                    <p><strong>Descripción:</strong> ${plan.descripcion_cuenta}</p>
                    <button class="modificar-plan-btn" data-id="${plan.id_plan_cuentas}" data-empresa-id="${empresaId}">Modificar</button>
                </div>
            `);
            planesDiv.append(planDiv);
        });

        planesDiv.on('click', '.modificar-plan-btn', function () {
            const planId = $(this).data('id');
            const empresaId = $(this).data('empresa-id');
            
            // Guarda el plan y empresa seleccionada en localStorage
            localStorage.setItem('planIdSeleccionado', planId);
            localStorage.setItem('empresaIdSeleccionada', empresaId);
        
            console.log("PlanId guardado:", localStorage.getItem('planIdSeleccionado'));
            console.log("EmpresaId guardado:", localStorage.getItem('empresaIdSeleccionada'));
        
            window.location.href = `modificar_plan.html`;
        });
    }

    function showCreatePlanButton() {
        const createButton = $("<button>Crear nuevo plan de cuentas</button>");
        createButton.click(function () {
            window.location.href = 'crear_plan.html';
        });
        $("#planes-de-cuentas").empty().append(createButton);
    }

    function showGenerarAsientosButton() {
        const generarAsientosBtn = $("<button id='generar-asientos-btn'>Generar Asientos Contables</button>");
        generarAsientosBtn.click(function () {
            window.location.href = 'generar_asientos.html'; // Redirige a la página de generar asientos contables
        });
        $("#asientos-contables-container").append(generarAsientosBtn);
    }

    function displaySearchResults(empresas) {
        const resultsDiv = $("#search-results");
        resultsDiv.empty();
        empresas.forEach(empresa => {
            console.log("Datos de la empresa:", empresa);
            const empresaDiv = $(`
                <div>
                    <span>${empresa.nombre}</span>
                    <button class="select-btn" data-id="${empresa.id_empresas}" data-nombre="${empresa.nombre}">Seleccionar</button>
                </div>
            `);
            resultsDiv.append(empresaDiv);
        });
    }

    // Manejo del botón para crear una nueva empresa
    $("#crear-empresa-btn").click(function () {
        window.location.href = 'crear_empresa.html';
    });
});
