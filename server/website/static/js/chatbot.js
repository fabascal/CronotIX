
function formatMessage(message) {
    // Reemplazar nuevas líneas por <br> para mantener los saltos de línea
    let formattedMessage = message.replace(/\n/g, '<br>');

    // Convertir listas numeradas en listas HTML
    formattedMessage = formattedMessage.replace(/(\d+)\. (Folio: \d+, Fecha: .+, Hora: .+, Total: .+)/g, '<li>$2</li>');
    
    // Envolver la lista con <ol> si hay elementos de lista
    if (formattedMessage.includes('<li>')) {
        formattedMessage = formattedMessage.replace(/<br>(<li>.+<\/li>)+<br>/g, '<ol>$&</ol>');
    }

    return formattedMessage;
};

function fillChat (data) {
    const formattedMessage = formatMessage(data.message);
    const mensajeHTML = `<div class="direct-chat-msg ${data.type === 'user' ? 'right' : ''}">
                <div class="direct-chat-infos clearfix">
                    <span class="direct-chat-name ${data.type === 'user' ? 'float-right' : 'float-left'}">${data.username}</span>
                    <span class="direct-chat-timestamp ${data.type === 'user' ? 'float-left' : 'float-right'}">${data.time}</span> <!-- Añade la hora si la tienes -->
                </div>
                <img class="direct-chat-img" src="/static/${data.image_url}" alt="Imagen de usuario">
                <div class="direct-chat-text">${formattedMessage}</div>
            </div>`;
    return mensajeHTML;
}
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('formMensaje');
    const mensajesContainer = document.getElementById('direct-chat-messages');
    const submitButton = document.getElementById('submit-button');
    const typingIndicator = document.getElementById('typingIndicator');
    const messageInput = document.getElementById('mensaje'); 

    form.onsubmit = function(e) {
        e.preventDefault();
        submitButton.disabled = true; // Deshabilita el botón para evitar doble clic

        let mensajeUsuario = form.mensaje.value.trim();
        if (mensajeUsuario) {
            // Muestra el mensaje del usuario en el chat
            let userData = {
                message: mensajeUsuario,
                type: 'user',
                time: formatDate(new Date()),
                username: form.getAttribute('data-username'),
                image_url: form.getAttribute('data-user-image')
            };
            mensajesContainer.innerHTML += fillChat(userData);
            mensajesContainer.scrollTop = mensajesContainer.scrollHeight; 
            messageInput.value = '';  // Limpia el campo de mensaje inmediatamente después de enviar

            // Muestra el indicador de escritura
            typingIndicator.style.display = 'block';

            let data = {
                message: mensajeUsuario,
                type: 'user',
                assistant_id: form.getAttribute('data-assistant-id')  
            };
            const csrf_token = document.querySelector('input[name="csrf_token"]').value;

            fetch('/enviar_mensaje', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrf_token,
                },
                body: JSON.stringify(data),
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                typingIndicator.style.display = 'none'; // Oculta el indicador de escritura
                mensajesContainer.innerHTML += fillChat(data); // Añade la respuesta del bot al chat
                mensajesContainer.scrollTop = mensajesContainer.scrollHeight; // Desplaza el chat hacia abajo
                messageInput.value = ''; // Limpia el input
            })
            .catch(error => console.error('Error:', error))
            .finally(() => {
                form.reset(); // Limpia el formulario
                submitButton.disabled = false; // Habilita el botón de enviar
            });
        } else {
            submitButton.disabled = false; // Habilita el botón si el mensaje está vacío
        }
    };
});

function formatAMPM(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // La hora '0' debe ser '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    let strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}

function formatDate(date) {
    const months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
    let day = date.getDate();
    let month = months[date.getMonth()];
    let formattedTime = formatAMPM(date);

    return day + ' ' + month + ' ' + formattedTime;
}