$(function () {
    //Registro, aunque por ahora no se va a utilizar.
    $("#registro").click(function (e) {
        e.preventDefault(); // Evitar que el formulario se envíe de forma tradicional
        alert("Por ahora el registro no esta habilitado")
        /*window.location.replace('src/plan_cuentas.html');
        const nombre = $("input[name='txt']").val();
        const correo = $("input[name='email']").val();
        const telefono = $("input[name='broj']").val();
        const contrasena = $("input[name='pswd']").val();
        const roles = 3
        const token = Math.random().toString(36).substring(2,12)
        $.ajax({
            url: 'http://localhost:5000/registro',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                nombre: nombre,
                correo: correo,
                telefono: telefono,
                clave: contrasena,
                roles_idroles: roles,
                token_idtoken: 0,
                recuperacion: token

            }),
            success: function (response) {
                alert('Usuario registrado con éxito');
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });*/

    });
    //Inicio de Sesion
    $("#login").click(function (e) { 
        e.preventDefault(); // Evitar que el formulario se envíe de forma tradicional
        const correo = $("#email").val();
        const contrasena = $("#password").val();
        if (correo === "" || contrasena === "") {
            alert("Por favor complete ambos campos.");
            return;
        }
    
    
        // Enviar datos a la dirección en Python
        $.ajax({
            url: 'http://localhost:9000/login/', // Asegúrate de que la URL es correcta
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                correo: correo,
                contrasena: contrasena
            }),
            success: function (response) {
                if (response.Falso === false) {
                    alert('Correo o clave incorrectos');
                } else {
                    alert('Inicio de sesión exitoso');
                    localStorage.setItem('correo',correo);
                    window.location.replace('src/menu.html');
                }
            },
            error: function (error) {
                console.error('Error:', error);
                alert('Error en el inicio de sesión');
            }
        });
    });

});