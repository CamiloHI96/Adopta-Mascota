// Función para verificar la disponibilidad del correo electrónico
function checkEmailAvailability() {
    var emailInput = document.getElementById('email');
    var emailMessage = document.getElementById('emailMessage');
    var email = emailInput.value;
    
    if (email.trim() === '') {
        emailInput.style.border = '';
        emailMessage.innerText = '';
        return;
    }
    
    // Realizar una solicitud AJAX al servidor para verificar la disponibilidad del correo electrónico
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/check_email_availability', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.available) {
                emailInput.style.border = '1px solid green';
                emailMessage.innerText = '';
            } else {
                emailInput.style.border = '1px solid red';
                emailMessage.innerText = 'Correo en uso';
            }
        }
    };
    xhr.send(JSON.stringify({email: email}));
}

// Controlador de eventos para restablecer el borde cuando el campo de correo electrónico está en blanco
document.getElementById('email').addEventListener('input', function() {
    var emailInput = this;
    var emailMessage = document.getElementById('emailMessage');
    if (emailInput.value.trim() === '') {
        emailInput.style.border = '';
        emailMessage.innerText = '';
    }
});