# Gemini-Backend-Clone
A Gemini-style backend system that enables user-specific chatrooms, OTP-based login, Gemini API-powered AI conversations, and subscription handling via Stripe. This project will assess your skills in backend architecture, authentication, third-party integration, and clean code practices.

---

## 🚀 Tech Stack

- **Language**: Python (Django)
- **Database**: PostgreSQL
- **Queue System**: Celery + Redis (Upstash)
- **Authentication**: JWT with OTP verification
- **Payments**: Stripe (Sandbox)
- **AI API**: Google Gemini
- **Deployment Platforms**: Render (main app & PostgreSQL), Railway (Celery worker), Upstash (Redis)

---

## 📦 Project Setup for local machine (Main Branch)

### 1. Clone the repository
```bash
git clone https://github.com/your-username/gemini-backend.git
cd gemini-backend
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Create a `.env` file with the following:
```env
SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=*


POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

STRIPE_SECRET_KEY=your_stripe_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret

GEMINI_API_KEY=your_gemini_key
```
Checkout .env.example for more details

### 5. Celery & Redis
A. Pull redis with docker & run
B. Run Celery
```bash
python -A celery gemini_backend worker -l info
```

### 6. Run database migrations
```bash
python manage.py migrate
```

### 7. Run the development server
```bash
python manage.py runserver
```

---

## 🧠 Architecture Overview

```
Clients ↔ Django Backend
         ↙         ↘
    PostgreSQL     Redis (Cache / Queue)
         ↓             ↓
      Stripe      Celery Worker (async Gemini)
```

- **Django** serves REST APIs with JWT-based authentication
- **Celery** runs async Gemini API calls and chat message generation
- **Redis** is used for both caching and Celery broker
- **Stripe** handles payment subscriptions
- **Upstash** is used for Redis, hosted serverlessly

---

## 📬 Queue System (Celery + Redis)

- Celery is configured to use Redis as a broker and result backend.
- Each chat message triggers a background task that calls Gemini API asynchronously.
- Redis is provisioned via **Upstash** and Celery worker is deployed using **Railway**.

---

## 🧠 Gemini API Integration

- When a user sends a message to a chatroom, a background task is queued.
- The Gemini API responds with a chat-like reply.
- The async task ensures fast frontend responsiveness and scalability.

---

## 🔐 Auth Endpoints

```http
POST /auth/signup/
POST /auth/send-otp/
POST /auth/verify-otp/
POST /auth/forgot-password/
POST /auth/change-password/
GET  /user/me/
```

## 💳 Subscription Endpoints (JWT protected)
```http
POST /subscribe/pro/
POST /webhook/stripe/
GET  /subscription/status/
GET  /payment/success/
```

## 💬 Chatroom Endpoints (JWT protected)
```http
POST /chatroom/
GET  /chatroom/
GET  /chatroom/<id>/
DELETE /chatroom/<id>/
POST /chatroom/<id>/message/
```

---

## ✅ Testing with Postman

1. Import the provided Postman collection (or create one). [Postman Collection link](https://documenter.getpostman.com/view/37555239/2sB34kEe9T#intro)
2. Register with `/auth/signup/`.
3. Use `/auth/send-otp/` and `/auth/verify-otp/`.
4. Create a chatroom and send messages.
5. Test subscription via Stripe sandbox.

---

## 🚀 Deployment Overview (See `render-deployment` Branch)

The `render-deployment` branch contains detailed setup instructions for:

- **Main Django App**: Hosted on [Render](https://render.com)
- **PostgreSQL**: Managed via Render's PostgreSQL add-on
- **Redis**: Provisioned using [Upstash](https://upstash.com)
- **Celery Worker**: Deployed using [Railway](https://railway.app)

👉 See more in the `render-deployment` branch

---

## 🧠 Design Decisions

- OTP-based JWT auth instead of email/password
- Async processing to avoid blocking request cycles
- Redis-based caching for chatroom listing
- Modular architecture for scalability

---

## 📎 Appendix

- This project is suitable for running on any public cloud
- Stripe is in sandbox mode; use test cards only

---

## 📄 License

MIT License

