document.addEventListener('DOMContentLoaded', (event) => {
    const copyIdButton = document.getElementById('copyIdButton');  
    const userId = copyIdButton.getAttribute('data-user-id');
    if (copyIdButton && userId) {
        copyIdButton.addEventListener('click', copyUserId);
    }
    function copyUserId() {
        navigator.clipboard.writeText(userId).then(() => {
            showFlashMessage('Id copiado con exito.', 'success');
        }).catch(err => {
            showFlashMessage('Error al copiar Id.', 'error');
        });
    }
});


function showFlashMessage(message, type) {
    Swal.fire({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        icon: type,
        title: message
    });
}

// Función para mostrar el spinner y el overlay
function showSpinner() {
    document.getElementById('spinner-overlay').style.display = 'block';
    document.getElementById('spinner').style.display = 'block';
}

// Función para ocultar el spinner y el overlay
function hideSpinner() {
    document.getElementById('spinner-overlay').style.display = 'none';
    document.getElementById('spinner').style.display = 'none';
}

