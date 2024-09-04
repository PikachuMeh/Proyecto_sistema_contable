$(document).ready(function () {
    const departamentos = [];

    const today = new Date();

    // Obtener el año actual, mes y día
    const maxYear = today.getFullYear();
    const maxMonth = String(today.getMonth() + 1).padStart(2, '0'); // Los meses en JavaScript van de 0 a 11
    const maxDay = String(today.getDate()).padStart(2, '0');
    const maxDate = `${maxYear}-${maxMonth}-${maxDay}`; // Fecha máxima es el día de hoy

    // Obtener la fecha de hace 100 años
    const minYear = maxYear - 100;
    const minDate = `${minYear}-${maxMonth}-${maxDay}`; // Fecha mínima es hace 100 años

    // Aplicar las validaciones de fecha
    $("#fecha_constitucion").attr("max", maxDate).attr("min", minDate);
    $("#fecha_ejercicio_economico").attr("max", maxDate);

    // Validar nombre de la empresa (solo texto)
    $("#nombre").on("input", function () {
        const value = $(this).val();
        if (/[^a-zA-Z\s]/.test(value)) {
            alert("El nombre de la empresa no debe contener números ni caracteres especiales.");
            $(this).val(value.replace(/[^a-zA-Z\s]/g, ""));
        }
    });

    // Validar RIF (nueve dígitos)
    $("#rif_numero").on("input", function () {
        const value = $(this).val();
        if (/[^0-9]/.test(value) || value.length > 9) {
            alert("El número de RIF debe contener solo números (9 dígitos).");
            $(this).val(value.replace(/[^0-9]/g, "").substring(0, 9));
        }
    });

    // Validar actividad económica (solo texto)
    $("#actividad_economica").on("input", function () {
        const value = $(this).val();
        if (/[^a-zA-Z\s]/.test(value)) {
            alert("La actividad económica no debe contener números ni caracteres especiales.");
            $(this).val(value.replace(/[^a-zA-Z\s]/g, ""));
        }
    });

    // Validar correo electrónico
    $("#correo").on("input", function () {
        const email = $(this).val();
        if (!validateEmail(email) && email !== "") {
            alert("Por favor, ingrese un correo electrónico válido.");
        }
    });

    // Función para validar correo electrónico
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }

    // Validar y agregar departamento a la lista
    $("#agregar-departamento-btn").click(function () {
        const nombreDepartamento = $("#nombre_departamento").val().trim();
        
        if (nombreDepartamento === "") {
            alert("El nombre del departamento no puede estar vacío.");
            return;
        }
    
        if (/[^a-zA-Z\s]/.test(nombreDepartamento)) {
            alert("El nombre del departamento solo debe contener letras y espacios.");
            return;
        }
    
        departamentos.push({ nombre_departamento: nombreDepartamento });
    
        actualizarListaDepartamentos();
        $("#nombre_departamento").val("");
    });
    
    // Función para actualizar la lista de departamentos
    function actualizarListaDepartamentos() {
        const lista = $("#lista-departamentos");
        lista.empty();
        departamentos.forEach((depto, index) => {
            lista.append(`
                <li>
                    ${depto.nombre_departamento} 
                    <button type="button" class="eliminar-departamento-btn" data-index="${index}">Eliminar</button>
                </li>
            `);
        });
    }

    // Eliminar un departamento de la lista
    $("#lista-departamentos").on("click", ".eliminar-departamento-btn", function () {
        const index = $(this).data("index");
        departamentos.splice(index, 1);
        actualizarListaDepartamentos();
    });

    // Validación y envío del formulario para crear la empresa
    $("#crearEmpresaForm").submit(function (event) {
        event.preventDefault(); // Evitar el envío predeterminado del formulario
    
        const tipoRif = $("#tipo_rif").val();
        const rifNumeros = $("#rif_numero").val();
        const rifCompleto = tipoRif + "-" + rifNumeros;
    
        const empresaData = {
            nombre: $("#nombre").val(),
            fecha_constitucion: $("#fecha_constitucion").val(),
            rif: rifCompleto,
            fecha_ejercicio_economico: $("#fecha_ejercicio_economico").val(),
            actividad_economica: $("#actividad_economica").val(),
            direccion: $("#direccion").val(),
            correo: $("#correo").val(),
            departamentos: departamentos
        };
    
        console.log(empresaData); // Agrega este log para revisar la estructura
    
        $.ajax({
            url: 'http://localhost:9000/empresas/crear',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(empresaData),
            success: function (response) {
                alert('Empresa y departamentos creados con éxito.');
                window.location.href = 'empresas.html';
            },
            error: function (error) {
                console.error('Error al crear la empresa:', error);
                alert('Hubo un error al crear la empresa.');
            }
        });
    });
    
});
