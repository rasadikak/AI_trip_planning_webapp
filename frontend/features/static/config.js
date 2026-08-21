const API_BASE = window.location.origin;

function handle401() {
    showToast("⚠️ Session timed out — please log in again", "error");
    setTimeout(() => {
        window.location.href = `${API_BASE}/frontend/home/login.html`;
    }, 2000);
}