# Snake Game - Deployment Guide

This guide covers deploying the Snake Game application using Docker, both locally and to cloud platforms.

## 🚀 Quick Start (Local)

### Prerequisites
- Docker and Docker Compose installed
- Git

### 1. Clone and Configure

```bash
git clone <your-repo-url>
cd snake-game-1

# Create environment file
cp .env.example .env

# Edit .env and change the secrets!
nano .env  # or use your preferred editor
```

**Important**: Change the `SECRET_KEY` and `POSTGRES_PASSWORD` in `.env` before deploying!

### 2. Build and Run

```bash
# Build and start all services
docker-compose up --build -d

# Check logs
docker-compose logs -f app

# Check service status
docker-compose ps
```

### 3. Access the Application

- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs
- **Database**: localhost:5432

### 4. Stop Services

```bash
docker-compose down        # Stop services
docker-compose down -v     # Stop and remove volumes (deletes database!)
```

---

## ☁️ Cloud Deployment

### Deploy to Render.com (Recommended)

Render provides free PostgreSQL and web service hosting with **one-click deployment** using the included `render.yaml` Blueprint.

#### Option A: One-Click Blueprint Deployment (Easiest)

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml` and show:
   - PostgreSQL database: `snake-game-db`
   - Web service: `snake-game`
6. Click **"Apply"** to deploy everything automatically

Your app will be live at `https://snake-game-<random>.onrender.com` in ~5 minutes.

#### Option B: Manual Deployment

##### 1. Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Fill in:
   - Name: `snake-game-db`
   - Database: `snake_game`
   - User: `snake_game_user`
   - Region: Choose closest to you
   - Plan: Free
4. Click "Create Database"
5. Copy the **Internal Database URL** (it starts with `postgresql://`)

##### 2. Deploy Application

1. Click "New +" → "Web Service"
2. Connect your Git repository
3. Configure:
   - **Name**: `snake-game`
   - **Environment**: Docker
   - **Region**: Same as database
   - **Branch**: main
   - **Dockerfile Path**: `./Dockerfile`
4. Add Environment Variables:
   ```
   DATABASE_URL=<paste-internal-database-url>
   SECRET_KEY=<generate-random-secret-key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ENVIRONMENT=production
   ```
5. Click "Create Web Service"

Your app will be live at `https://snake-game-<random>.onrender.com`

**Note**: Free tier goes to sleep after inactivity. First request may take 30-60s.

---

### Deploy to Railway.app

Railway offers simple deployment with automatic PostgreSQL provisioning.

#### Steps:

1. Go to [Railway](https://railway.app/)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Docker
5. Add PostgreSQL:
   - Click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway automatically sets `DATABASE_URL`
6. Add environment variables to your web service:
   ```
   SECRET_KEY=<generate-random-secret-key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ENVIRONMENT=production
   ```
7. Deploy!

Your app will be at `https://<project-name>.up.railway.app`

---

### Deploy to Fly.io

Fly.io offers global deployment with excellent performance.

#### 1. Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://fly.io/install.ps1'))"
```

#### 2. Login and Initialize

```bash
flyctl auth login
flyctl launch --no-deploy
```

Answer the prompts:
- App name: `snake-game-<your-name>`
- Region: Choose closest
- PostgreSQL: Yes (this creates a free PostgreSQL database)
- Redis: No

#### 3. Set Secrets

```bash
flyctl secrets set SECRET_KEY=$(openssl rand -hex 32)
flyctl secrets set ALGORITHM=HS256
flyctl secrets set ACCESS_TOKEN_EXPIRE_MINUTES=30
flyctl secrets set ENVIRONMENT=production
```

#### 4. Deploy

```bash
flyctl deploy
```

Your app will be at `https://snake-game-<your-name>.fly.dev`

---

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes (cloud) | `sqlite:///./snake_game.db` |
| `SECRET_KEY` | JWT signing secret | Yes | - |
| `ALGORITHM` | JWT algorithm | No | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | No | `30` |
| `POSTGRES_USER` | Database user | No | `postgres` |
| `POSTGRES_PASSWORD` | Database password | No | `postgres` |
| `POSTGRES_DB` | Database name | No | `snake_game` |
| `ENVIRONMENT` | App environment | No | `production` |

---

## 🛠️ Development vs Production

### Development (Local with SQLite)
```bash
# Backend
cd backend
uv run uvicorn main:app --reload --port 3000

# Frontend
cd frontend
npm run dev
```

### Production (Docker)
```bash
docker-compose up --build
```

---

## 📊 Monitoring & Logs

### Docker Compose Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f db
```

### Database Access
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d snake_game

# Backup database
docker-compose exec db pg_dump -U postgres snake_game > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres snake_game < backup.sql
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Change `POSTGRES_PASSWORD` to a strong password
- [ ] Use HTTPS in production (cloud platforms provide this automatically)
- [ ] Review CORS settings in `backend/main.py`
- [ ] Enable database backups
- [ ] Set up monitoring/alerting

---

## 🐛 Troubleshooting

### Application won't start
```bash
# Check logs
docker-compose logs app

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Database connection errors
```bash
# Check database is running
docker-compose ps

# Test database connection
docker-compose exec app pg_isready -h db
```

### Port already in use
```bash
# Change port in docker-compose.yml
# ports:
#   - "8081:8080"  # Use 8081 instead of 8080
```

---

## 📦 Architecture

```
┌─────────────────────────────────────┐
│         Docker Container            │
├─────────────────────────────────────┤
│  Nginx (Port 8080)                  │
│    ↓                                │
│    ├─ Static Files (Frontend)      │
│    └─ /api/* → FastAPI (Port 3000) │
│                                     │
│  FastAPI Backend                    │
│    ↓                                │
│  PostgreSQL Database                │
└─────────────────────────────────────┘
```

---

## 🎯 Performance Tips

1. **Enable CDN**: Most cloud platforms offer CDN. Enable it for static assets.
2. **Database Indexing**: Already configured in `models.py`
3. **Connection Pooling**: FastAPI uses SQLAlchemy connection pooling
4. **Nginx Caching**: Configured in `nginx.conf`
5. **Scaling**: Increase workers in `docker-entrypoint.sh` (change `--workers 2` to higher)

---

## 📝 License

MIT License - See LICENSE file for details
