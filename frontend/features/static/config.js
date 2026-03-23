const API_BASE = "http://127.0.0.1:8000";

function handle401() {
    showToast("⚠️ Session timed out — please log in again", "error");
    setTimeout(() => {
        window.location.href = `${API_BASE}/frontend/home/login.html`;
    }, 2000);
}