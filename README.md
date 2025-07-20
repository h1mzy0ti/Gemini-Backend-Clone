# Gemini-Backend-Clone
A Gemini-style backend system that enables user-specific chatrooms, OTP-based login, Gemini API-powered AI conversations, and subscription handling via Stripe. This project will assess your skills in backend architecture, authentication, third-party integration, and clean code practices.

# Deployment Guide

This document outlines the deployment details for each component of the Gemini Backend Clone project.

---

## 🌐 Deployment Overview

| Component      | Platform | URL / Details                                                      |
| -------------- | -------- | ------------------------------------------------------------------ |
| Django Backend | Render   | [https://gemini-backend-clone-xyqy.onrender.com]                   |
| PostgreSQL     | Render   | Managed PostgreSQL Database                                        |
| Redis (Broker) | Upstash  | `rediss://default:<token>@<host>:6379`                             |
| Celery Worker  | Railway  | Deployed as background worker                                      |

> 🔗 See main project README for overall architecture and setup instructions.

# Note

Since I am using an free instance in Render it the instance will spin down with inactivity, which can delay requests by 50 seconds or more.
---

## 🔧 Environment Variables

All deployment environments must include

1. In the render env variable
2. Railway env variable

Refer .env.example


---

## 🚀 Render Deployment (Backend + PostgreSQL)

### Django Backend:

- Deployed using Gunicorn and Python 3.11
- Auto-deploys on push to `render-deployment` branch
- Uses environment variables as listed above

### PostgreSQL:

- Use Render’s managed PostgreSQL service
- Set `DATABASE_URL` in the backend's environment

---

## ⚡️ Redis via Upstash

- Used as broker and result backend for Celery
- Secure connection using `rediss://` protocol
- No need to run Redis yourself

Example:

```env
REDIS_URL=rediss://default:<token>@<host>:6379
```

---

## 🧵 Celery Worker via Railway

- Clone the repo to Railway
- Set the same environment variables as backend
- Railway worker command:

```bash
celery -A gemini_backend worker --loglevel=info
```

- Make sure the branch is `render-deployment` for consistency

---

## 📬 Stripe Webhooks

- Stripe webhook endpoint:
  ```
  https://<your-domain>/webhook/stripe/
  ```
- Set `STRIPE_WEBHOOK_SECRET` for signature verification

---

## 🧪 Testing Post Deployment

Use Postman with the following base URL:

```
https://<your-domain>/ or demo deployment > https://gemini-backend-clone-xyqy.onrender.com
```

Test the following endpoints:

- `/auth/signup/`
- `/auth/send-otp/`
- `/auth/verify-otp/`
- `/chatroom/`
- `/chatroom/:id/message/`
- `/subscribe/pro/`

---

## ✅ Final Notes

- All critical deployment info is stored in this branch (`render-deployment`)
- See README.md for project overview
- Ensure worker and backend point to the same Redis broker



