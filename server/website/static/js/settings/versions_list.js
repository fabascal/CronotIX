document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll('#models-data tbody tr');
    rows.forEach(row => {
        row.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
});