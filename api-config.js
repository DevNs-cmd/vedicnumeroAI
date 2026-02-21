// ============================================================
// NumerAI – API Configuration
// Change API_BASE_URL below to your deployed backend URL
// before pushing to production (Vercel, Railway, Render, etc.)
// ============================================================

const API_BASE_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000"
  : "https://your-backend-api.onrender.com"; // <-- Replace with your deployed API URL

// Make available globally
window.API_BASE_URL = API_BASE_URL;
