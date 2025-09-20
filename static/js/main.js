// Custom project-wide JavaScript can be added here.

document.addEventListener("DOMContentLoaded", function() {
    // Sidebar toggle functionality
    const sidebarToggle = document.body.querySelector("#sidebarToggle");
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", function(event) {
            event.preventDefault();
            document.body.classList.toggle("sb-sidenav-toggled");
        });
    }

    // HTMX Toast Notification Listener
    const toastElement = document.getElementById('appToast');
    if (toastElement) {
        const appToast = new bootstrap.Toast(toastElement);

        document.body.addEventListener('showToast', function(event) {
            // Get message from the event detail
            const message = event.detail.message || "Action completed successfully!";
            toastElement.querySelector('.toast-body').textContent = message;
            appToast.show();
        });
    }
});