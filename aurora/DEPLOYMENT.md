# AURORA Deployment & Setup Guide

This guide covers how to get AURORA running locally and in production.

## Prerequisites
- Docker and Docker Compose (recommended)
- Node.js 20+ (for manual frontend setup)
- Python 3.12+ (for manual backend setup)
- A FRED API Key ([get one for free here](https://fred.stlouisfed.org/docs/api/api_key.html))

---

## 🚀 Quick Start (Docker Compose)
The easiest way to run the full stack (Frontend, Backend, and Database) is using Docker Compose.

1. **Clone the repository.**
2. **Set up environment variables:**
   Create a `.env` file in the root `aurora` directory (or set them in your shell):
   ```bash
   FRED_API_KEY=your_api_key_here
   ```
3. **Run the application:**
   ```bash
   docker-compose up --build
   ```
4. **Access the apps:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠️ Manual Setup (Development)

### 1. Backend (FastAPI)
1. Navigate to `apps/api`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file based on `.env.example`.
4. Run the server: `uvicorn main:app --reload`.

### 2. Frontend (Next.js)
1. Navigate to `apps/web`.
2. Install dependencies: `npm install`.
3. Create a `.env` file based on `.env.example`.
4. Run the server: `npm run dev`.

---

## ☁️ Production Deployment

### Frontend (Vercel)
1. Connect your repository to Vercel.
2. Set the **Root Directory** to `aurora/apps/web`.
3. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend (e.g., `https://aurora-api.onrender.com`).

### Backend (Render / Railway / Fly.io)
1. Create a new Web Service.
2. Set the **Root Directory** to `aurora/apps/api` (or use the root and point to the `Dockerfile`).
3. Add Environment Variables:
   - `DATABASE_URL`: Your PostgreSQL connection string (e.g., from Supabase or Neon).
   - `FRED_API_KEY`: Your FRED API key.
4. The backend will automatically create tables on startup.

### Google Cloud Platform (Full Stack Streamlined)

Google Cloud can host the entire stack. To streamline it, use **Firebase Hosting** for the frontend and **Cloud Run** for the backend.

#### 1. Database: Google Cloud SQL (PostgreSQL)
- Create a **Cloud SQL for PostgreSQL** instance.
- Create a database named `aurora_db`.
- **Note:** Cloud SQL is not free. For a free hackathon alternative, use **Neon.tech** or **Supabase**.

#### 2. Backend: Cloud Run
- Enable the Cloud Run and Cloud Build APIs.
- Deploy the backend:
  ```bash
  cd aurora/apps/api
  gcloud builds submit --tag gcr.io/[PROJECT_ID]/aurora-api
  gcloud run deploy aurora-api --image gcr.io/[PROJECT_ID]/aurora-api --platform managed --allow-unauthenticated --set-env-vars "DATABASE_URL=[DB_URL],FRED_API_KEY=[KEY]"
  ```

#### 3. Frontend: Firebase Hosting (Recommended for Next.js)
- Install Firebase CLI: `npm install -g firebase-tools`.
- Run `firebase init` in `aurora/apps/web` and choose **Hosting**.
- Choose "Set up as a single-page app" and "Set up automatic builds and deploys with GitHub".
- **Streamlining Tip:** Firebase can automatically proxy requests to your Cloud Run backend using a `rewrites` rule in `firebase.json`.

---

### Database (Supabase / Neon / Cloud SQL)
1. Create a free PostgreSQL instance on [Supabase](https://supabase.com) or [Neon](https://neon.tech).
2. Copy the connection string and use it as `DATABASE_URL` for the backend.

---

## 📁 Project Structure
- `apps/api`: FastAPI backend with SQLAlchemy models.
- `apps/web`: Next.js frontend with Tailwind CSS and Framer Motion.
- `packages/database`: Shared database schema (Prisma).
