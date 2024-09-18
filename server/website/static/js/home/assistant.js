document.addEventListener('DOMContentLoaded', (event) => {
    const apiKeyButtons = document.querySelectorAll('[id^="ApiKeyAssistantCopy-"]');

    apiKeyButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const assistantId = button.id.split('-')[1];
            const idField = document.getElementById(`assistant-id-${assistantId}`);

            fetch(`/ApiKeyAssistantCopy/${assistantId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
                }
            })
            .then(response => response.json())
            .then(data => {
                navigator.clipboard.writeText(data.apikey)
                showFlashMessage('API Key copiado con exito.', 'success');
            })
            .catch(error => 
                showFlashMessage('Error al copiar API Key.', 'success'),
                console.error('Error al copiar la API Key:', error));
        });
    });
});
