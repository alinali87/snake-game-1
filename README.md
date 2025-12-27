# Snake Game - Full Stack Application

A classic Snake game built with React + TypeScript + Vite frontend and FastAPI + SQLAlchemy backend.

## Features

- 🎮 Classic snake gameplay with arrow key controls
- 🏆 Real-time leaderboard with user authentication
- 🎯 Two game modes: Walls (harder) and Pass-Through (easier)
- 👤 User authentication with JWT tokens
- 📊 Comprehensive user statistics and game history
- 🎨 Modern, responsive UI with dark theme
- 🚀 Production-ready Docker deployment
- 🧪 Comprehensive test coverage (100%)

## Tech Stack

### Frontend
- React 19
- TypeScript
- Vite
- CSS3

### Backend
- FastAPI
- Python 3.11
- SQLAlchemy
- PostgreSQL / SQLite database
- JWT Authentication
- Pytest for testing

### DevOps
- Docker & Docker Compose
- Nginx reverse proxy
- Multi-stage builds
- PostgreSQL for production

## Project Structure

```
snake-game-1/
├── frontend/           # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── App.tsx    # Main game component
│   │   ├── App.css    # Game styling
│   │   └── main.tsx   # Entry point
│   └── vite.config.ts # Vite configuration (port 8080)
├── backend/           # FastAPI backend
│   ├── main.py        # FastAPI app with CORS
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic schemas
│   ├── database.py    # Database configuration
│   └── requirements.txt
└── package.json       # Root package with concurrent scripts
```

## Quick Start

### Development (Local)

See [Setup Instructions](#setup-instructions) below for detailed local development setup.

### Production (Docker)

```bash
# Clone the repository
git clone <repository-url>
cd snake-game-1

# Create environment file
cp .env.example .env
# Edit .env and set your SECRET_KEY and POSTGRES_PASSWORD

# Start with Docker Compose
docker-compose up -d

# Access the application at http://localhost:8080
```

For detailed deployment guides (Render, Railway, Fly.io), see [DEPLOYMENT.md](./DEPLOYMENT.md).

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Python 3.11 or higher
- npm or yarn
- uv (Python package manager) - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**For Docker deployment:**
- Docker & Docker Compose
- PostgreSQL (handled by docker-compose)

### Installation

1. Install root dependencies:
```bash
npm install
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
cd ..
```

3. Install backend dependencies (using uv):
```bash
cd backend
uv venv
uv pip install -r requirements.txt
cd ..
```

Or install all dependencies at once:
```bash
npm run install:all
```

### Running the Application

#### Option 1: Run both servers concurrently (recommended)
```bash
npm run dev
```

#### Option 2: Run servers separately

Terminal 1 - Frontend (port 8080):
```bash
npm run dev:frontend
```

Terminal 2 - Backend (port 3000):
```bash
npm run dev:backend
```

### Access the Application

- Frontend: http://localhost:8080
- Backend API: http://localhost:3000
- API Docs: http://localhost:3000/docs

## How to Play

1. Click "Start Game" to begin
2. Use arrow keys to control the snake:
   - ↑ Up Arrow: Move up
   - ↓ Down Arrow: Move down
   - ← Left Arrow: Move left
   - → Right Arrow: Move right
3. Eat the red food to grow and increase your score
4. Avoid hitting the walls or yourself
5. When game ends, save your score to the leaderboard

## API Endpoints

- `GET /api/scores` - Get top 10 high scores
- `POST /api/scores` - Create a new score
- `GET /api/scores/{id}` - Get a specific score

## Configuration

### Ports
- Frontend: 8080 (configured in `frontend/vite.config.ts`)
- Backend: 3000 (configured in root `package.json`)
- Production (Docker): 8080 (Nginx serves frontend and proxies /api/* to backend)

### CORS
CORS is configured in `backend/main.py` to allow requests from `http://localhost:8080`

### Database
- **Development**: SQLite database (`snake_game.db`) is created automatically in the `backend/` directory on first run.
- **Production**: PostgreSQL database (configured via `DATABASE_URL` environment variable)

### Environment Variables
Create a `.env` file for production deployment:
```bash
SECRET_KEY=your-secret-key-here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=snake_game
```

See `.env.example` for a complete template.

## Development

### Frontend Development
The frontend uses Vite's hot module replacement for instant updates during development.

### Backend Development
The backend uses Uvicorn with `--reload` flag for automatic reloading on code changes. The project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

## Testing

The project includes comprehensive test coverage (100% passing):

### Backend Tests (pytest)
```bash
cd backend
pytest
```

**Coverage:** 19 tests covering authentication, game CRUD operations, and leaderboard functionality.

### Frontend Tests (vitest)
```bash
cd frontend
npm test
```

**Coverage:** 25 tests covering game logic, movement, collision detection, and scoring.

For detailed test results, see [README_TESTS.md](./README_TESTS.md).

## Deployment

This application supports multiple deployment options:

- **Docker Compose** (recommended): Local and cloud deployment with PostgreSQL
- **Render.com**: Web service deployment with PostgreSQL
- **Railway.app**: One-click deployment from GitHub
- **Fly.io**: Global edge deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions for each platform.

## Future Enhancements

- Add difficulty levels
- Implement pause functionality
- Add sound effects
- Mobile touch controls
- Multiplayer mode

## License

MIT
