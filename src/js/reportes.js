$(document).ready(function () {
    // Mostrar u ocultar los campos según el tipo de reporte seleccionado
    $('#tipo_reporte').change(function () {
        const tipoReporte = $(this).val();
        if (tipoReporte === 'diario') {
            $('#fecha_diaria').show();
            $('#mes_mensual').hide();
        } else if (tipoReporte === 'mensual') {
            $('#fecha_diaria').hide();
            $('#mes_mensual').show();
        }
    });

    // Manejar la generación del reporte
    $('#generar_reporte_btn').click(function () {
        const tipoReporte = $('#tipo_reporte').val();
        let fecha = null;

        if (tipoReporte === 'diario') {
            fecha = $('#fecha_reporte').val();
        } else if (tipoReporte === 'mensual') {
            fecha = $('#mes_reporte').val();
        }

        if (!fecha) {
            alert("Por favor, seleccione la fecha o el mes para el reporte.");
            return;
        }

        $.ajax({
            url: `http://localhost:9000/reportes/${tipoReporte}`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ fecha: fecha }),
            success: function (response) {
                mostrarReporte(response);
            },
            error: function (error) {
                console.error('Error al generar el reporte:', error);
                if (error.responseJSON && error.responseJSON.detail) {
                    alert(`Error: ${error.responseJSON.detail}`);
                } else {
                    alert('Hubo un problema al generar el reporte.');
                }
            }
        });
    });

    // Mostrar el reporte en el DOM
    function mostrarReporte(reporte) {
        $('#resultado_reporte').empty();

        if (reporte.length === 0) {
            $('#resultado_reporte').append('<p>No se encontraron asientos cerrados para este período.</p>');
        } else {
            let reporteHTML = '<h3>Reporte Generado</h3>';

            reporte.forEach(asiento => {
                reporteHTML += `<h4>Asiento ${asiento.num_asiento}</h4>`;
                reporteHTML += `<p>Apertura: ${asiento.fecha_apertura}</p>`;
                reporteHTML += `<p>Cierre: ${asiento.fecha_cierre}</p>`;
                reporteHTML += '<ul>';
                let totalDebe = 0;
                let totalHaber = 0;
                
                asiento.cuentas.forEach(cuenta => {
                    reporteHTML += `<li>${cuenta.descripcion_cuenta}: Debe ${cuenta.debe}, Haber ${cuenta.haber}</li>`;
                    totalDebe += cuenta.debe;
                    totalHaber += cuenta.haber;
                });

                reporteHTML += '</ul>';
                reporteHTML += `<p><strong>Total Debe:</strong> ${totalDebe}</p>`;
                reporteHTML += `<p><strong>Total Haber:</strong> ${totalHaber}</p>`;
            });

            $('#resultado_reporte').append(reporteHTML);
        }
    }

    // Botón para volver al menú principal
    $('#volver_btn').click(function () {
        window.location.href = 'menu.html';
    });
});
