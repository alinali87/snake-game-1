# Snake Game - Full Stack Application

A classic Snake game built with React + TypeScript + Vite frontend and FastAPI + SQLAlchemy backend.

## Features

- Classic snake gameplay with arrow key controls
- Real-time score tracking
- High score leaderboard with persistent storage
- Modern, responsive UI with dark theme
- Full-stack architecture with REST API

## Tech Stack

### Frontend
- React 19
- TypeScript
- Vite
- CSS3

### Backend
- FastAPI
- Python 3.x
- SQLAlchemy
- SQLite database

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

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8 or higher
- npm or yarn
- uv (Python package manager) - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

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

### CORS
CORS is configured in `backend/main.py` to allow requests from `http://localhost:8080`

### Database
SQLite database (`snake_game.db`) is created automatically in the `backend/` directory on first run.

## Development

### Frontend Development
The frontend uses Vite's hot module replacement for instant updates during development.

### Backend Development
The backend uses Uvicorn with `--reload` flag for automatic reloading on code changes. The project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

## Future Enhancements

- Add difficulty levels
- Implement pause functionality
- Add sound effects
- Mobile touch controls
- Multiplayer mode
- User authentication

## License

MIT
