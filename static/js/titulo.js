// Importar el archivo JavaScript de typed.js
var script = document.createElement('script');
script.src = 'https://unpkg.com/typed.js@2.1.0/dist/typed.umd.js';

// Esperar a que se cargue typed.js antes de continuar
script.onload = function() {
  // Inicializar Typed para el título
  var typed = new Typed(".auto-type", {
    strings: ["ADOPTA MASCOTA", "A TU COMPAÑERO DE VIDA"],
    cursorChar: '',
    startDelay: 0,
    tySpeed: 0,
    backSpeed: 400,
    loop: true
  });
};
document.head.appendChild(script);