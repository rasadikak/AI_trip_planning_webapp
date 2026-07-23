# 🌴 Serendib AI — Sri Lanka Trip Planner

> An AI-powered full-stack travel planning platform that generates personalized Sri Lanka itineraries using LLMs, with integrated weather, currency conversion, image-based destination search, and a real-time travel assistant.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📖 Overview

Serendib AI is a full-stack web application that helps travelers plan personalized trips across Sri Lanka. It combines a LangChain-powered AI agent, computer vision, and several real-time data APIs into a single cohesive trip-planning experience — complete with secure authentication, saved itineraries, and PDF export.

---

## ✨ Features

### 🤖 AI Trip Planner
- Generates detailed, day-by-day itineraries using a **LangChain ReAct Agent**
- Powered by **Gemini API**
- Considers destination type, budget, number of travelers, accommodation, and food preferences
- Includes cost estimates in LKR, transport options, accommodation suggestions, and Google Maps links
- Integrated **weather tool** the agent calls automatically for the main destination
- Rate-limited to prevent abuse (`slowapi`)

### 💬 AI Travel Assistant (Chatbot)
- Conversational assistant scoped strictly to Sri Lanka travel topics
- Persists conversation history **per user** in PostgreSQL
- Automatically trims history to the last N messages per user
- Input sanitization against prompt injection attempts
- Built using the OpenAI SDK client pointed at HuggingFace's inference router

### 🖼️ Image-Based Destination Search
- Upload any photo and identify the matching Sri Lankan destination
- Powered by **OpenAI CLIP (ViT-B/32)** for image embeddings
- Similarity search via vector indexing (FAISS)
- Returns top-matching destinations with confidence scores

### 🌤️ Live Weather
- Real-time weather lookup for any Sri Lankan destination
- Temperature, humidity, wind speed, visibility, and UV index
- No API key required (wttr.in)

### 💱 Currency Converter
- Converts LKR to 160+ world currencies
- Live exchange rates (open.er-api.com)
- Searchable currency picker with autocomplete

### 📄 PDF Export
- Converts any generated itinerary into a polished, downloadable PDF
- Custom font handling for emoji and Unicode rendering (`fpdf2` + DejaVu/NotoEmoji fonts)
- Color-coded headings and structured formatting

### 💾 Trip Management
- **Save plans** — store full itineraries tied to the user's account
- **Favourite places** — bookmark specific destinations from any generated plan
- Re-download saved plans as PDF at any time
- Full CRUD with duplicate detection

### 🔐 Authentication & Account Security
- **JWT-based authentication** stored in `httponly` cookies (not exposed to JS)
- Three separate JWT secrets/algorithms for: login sessions, password reset, and email verification — isolating token scopes
- **Email verification on signup** — accounts must verify before logging in
- **Password reset flow** — secure, time-limited reset links sent via email
- **bcrypt** password hashing
- Resend verification email if user forgets to verify
- Inline profile editing (name) with live validation
- **Account deletion** with cascading delete (removes all chat history, saved plans, and favourites)
- Session timeout handling — automatic redirect to login on token expiry
- Password visibility toggle (Font Awesome eye icon) on all password fields

### 📊 Logging & Observability
- Structured logging across all routers (`INFO`, `WARNING`, `ERROR`, `CRITICAL` levels)
- Daily rotating log files
- Request-level logging middleware (method, path, status code, response time)
- Startup/shutdown lifecycle logging

### 🎨 Frontend
- Fully responsive UI built with **Tailwind CSS** (CLI-based production build)
- Custom **Tropical Green** design theme
- Toast notification system (Toastify.js) replacing all native `alert()` calls
- Markdown rendering for AI-generated content (`marked.js`)
- No page reloads for any core action — all forms use `fetch()` with JSON/FormData

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | Core web framework / REST API |
| **SQLAlchemy** | ORM for PostgreSQL |
| **Alembic** | Database migrations |
| **PostgreSQL** | Primary relational database |
| **Pydantic** | Data validation & settings management |
| **python-jose** | JWT encoding/decoding |
| **passlib (bcrypt)** | Password hashing |
| **fastapi-mail** | Transactional email sending (verification, password reset) |
| **slowapi** | Rate limiting |
| **uvicorn** | ASGI server |

### AI / Machine Learning
| Technology | Purpose |
|---|---|
| **LangChain** | ReAct agent orchestration for trip planning |
| **HuggingFace Inference API (Novita provider)** | Hosting for Llama 3.1 8B Instruct |
| **OpenAI Python SDK** | Client interface to HuggingFace's OpenAI-compatible router |
| **OpenAI CLIP (ViT-B/32)** | Image embedding generation for visual search |
| **FAISS** | Vector similarity search for image-based destination matching |

### Frontend
| Technology | Purpose |
|---|---|
| **HTML5 / CSS3 / Vanilla JavaScript** | Core frontend (no framework) |
| **Tailwind CSS (CLI build)** | Utility-first styling, production-minified |
| **Toastify.js** | Non-blocking toast notifications |
| **marked.js** | Markdown → HTML rendering for AI responses |
| **Font Awesome** | Icon system (password toggle, navigation icons) |
| **Google Fonts** (Playfair Display, Outfit) | Typography |

### External APIs
| API | Purpose |
|---|---|
| **wttr.in** | Weather data |
| **open.er-api.com** | Currency exchange rates |
| **Nominatim (OpenStreetMap)** | Geocoding |

### DevOps & Tooling
| Tool | Purpose |
|---|---|
| **Git / GitHub** | Version control |
| **GitHub Actions** | CI/CD pipeline (test → build → deploy) |
| **pytest + httpx** | Automated backend testing |
| **Supabase** | Managed PostgreSQL hosting |
| **Python logging module** | Structured application logs |

---

## 🔑 Authentication Flow

```
Register → Email verification link sent → User verifies → Can log in

Login    → Credentials validated → JWT issued → Stored in httponly cookie

Request  → Cookie sent automatically → JWT verified → current_user resolved

Logout   → Cookie cleared → Redirect to home
```

Three isolated JWT scopes are used:
- **Login sessions** — short-lived access tokens
- **Password reset** — single-use, time-limited tokens (15 min expiry)
- **Email verification** — single-use, time-limited tokens (30 min expiry)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- Node.js (for Tailwind CSS build)
- HuggingFace API token
- SMTP credentials (for email sending)

### Installation

```bash
# Clone the repository
git clone https://github.com/rasadikak/AI_trip_planning_webapp.git
cd serendib-ai

# Create virtual environment
python -m venv env
source env/bin/activate      # Windows: env\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install

# Build Tailwind CSS
npx tailwindcss -i ./frontend/static/css/input.css -o ./frontend/static/css/output.css --watch
```

### Environment Variables

Create a `.env` file in the project root:

```env
SQLALCHEMY_DATABASE_URL=postgresql://user:password@localhost/serendib_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

SECRET_KEY2=your_reset_password_secret
ALGORITHM2=HS256
ACCESS_TOKEN_EXPIRE_TIME2=15

SECRET_KEY3=your_email_verification_secret
ALGORITHM3=HS256
ACCESS_TOKEN_EXPIRE_MINUTES3=30

GEMINI_API_KEY=your_gemini_api_key
BASE_URL=http://127.0.0.1:8000

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

### Database Setup

```bash
alembic upgrade head
```

### Run the Application

```bash
uvicorn backend.main:app --reload
```

Visit `http://127.0.0.1:8000/frontend/home/home.html`

---

## 🧪 Testing

```bash
pytest tests/ -v
```

Test coverage includes:
- Authentication flows (registration validation, login errors)
- Weather endpoint (valid/invalid destinations)
- Trip planner input validation
- Authorization checks (401 responses on protected routes)
- PDF generation

---

## 📦 Deployment

This project is configured for CI/CD via **GitHub Actions**:

1. Push to `main` triggers automated tests
2. Tailwind CSS is rebuilt and minified
3. On success, deployment is triggered via Render.com deploy hooks

See `.github/workflows/deploy.yml` for the full pipeline.

---

## 📝 License

This project is licensed under the MIT License.
