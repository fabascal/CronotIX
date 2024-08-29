function fillChat (data) {
    const mensajeHTML = `
			<div class="chat-message clearfix">
              
              <img src="static/${data.image_url}" alt="Imagen de usuario" width="32" height="32">
    
              <div class="chat-message-content clearfix">
                
                <span class="chat-time">${data.time}</span>
    
                <h5>${data.username}</h5>
    
                <p>${data.message}</p>
    
              </div> <!-- end chat-message-content -->
    
            </div> <!-- end chat-message -->
    
            <hr>`;
    return mensajeHTML;
};


(function() {
	

	$('#live-chat header').on('click', function() {

		$('.chat').slideToggle(300, 'swing');
		$('.chat-message-counter').fadeToggle(300, 'swing');

	});

	$('.chat-close').on('click', function(e) {

		e.preventDefault();
		$('#live-chat').fadeOut(300);

	});

	document.addEventListener("DOMContentLoaded", function() {

		form = document.getElementById('formMensaje');	
		const mensajesContainer = document.getElementById('direct-chat-messages');
		const messageInput = document.getElementById('mensaje'); 
		const csrf_token = document.querySelector('input[name="csrf_token"]').value;


		form.onsubmit = function(e) {
			e.preventDefault();
			let mensajeUsuario = form.mensaje.value.trim();
			console.log(mensajeUsuario);
			if (mensajeUsuario) {
				let userData = {
					message: mensajeUsuario,
					type: 'user',
					time: formatDate(new Date()),
					username: form.getAttribute('data-username'),
					image_url: form.getAttribute('data-user-image')
				};
				mensajesContainer.innerHTML += fillChat(userData);
				mensajesContainer.scrollTop = mensajesContainer.scrollHeight; 
				messageInput.value = '';  

				let data = {
					message: mensajeUsuario,
					type: 'user'
				};
				
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
					mensajesContainer.innerHTML += fillChat(data); // Añade la respuesta del bot al chat
					mensajesContainer.scrollTop = mensajesContainer.scrollHeight; // Desplaza el chat hacia abajo
					messageInput.value = ''; // Limpia el input
				})
				.catch(error => console.error('Error:', error))
				.finally(() => {
					form.reset(); // Limpia el formulario
				});
			};

		};
	});

}) ();
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