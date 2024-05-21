// Obtener referencia al formulario
var formulario = document.getElementById('refugio-form');


formulario.addEventListener('submit', function (event) {
    event.preventDefault();

    var nombre = document.getElementById('nombre').value;
    var direccion = document.getElementById('direccion').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/agregar_refugio', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            alert('Refugio agregado exitosamente');
        } else {
            alert('Error al agregar refugio');
        }
    };
    xhr.send(JSON.stringify({ nombre: nombre, direccion: direccion }));
});
