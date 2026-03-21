function showToast(message, type = "success") {
    const colors = {
        success : "#2E7D32",   // green
        error   : "#c62828",   // red
        info    : "#1565C0",   // blue
        warning : "#e65100"    // orange
    };

    Toastify({
        text: message,
        duration: 10000,
        gravity: "top",
        position: "right",
        stopOnFocus: true,
        style: {
            background: colors[type] || colors.success,
            borderRadius: "8px",
            fontSize: "0.9rem",
            padding: "12px 20px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.3)"
        }
    }).showToast();
}