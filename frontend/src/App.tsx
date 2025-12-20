import { useState, useEffect, useCallback } from "react";
import "./App.css";
import { useAuth } from "./contexts/AuthContext";
import { AuthForms } from "./components/AuthForms";
import { Leaderboard } from "./components/Leaderboard";

interface Position {
  x: number;
  y: number;
}

type Direction = "UP" | "DOWN" | "LEFT" | "RIGHT";
type GameMode = "walls" | "pass-through";

const GRID_SIZE = 20;
const CELL_SIZE = 20;
const INITIAL_SNAKE: Position[] = [{ x: 10, y: 10 }];
const INITIAL_DIRECTION: Direction = "RIGHT";
const GAME_SPEED = 150;

function App() {
  const { user, token, logout, isAuthenticated, isLoading } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [snake, setSnake] = useState<Position[]>(INITIAL_SNAKE);
  const [food, setFood] = useState<Position>({ x: 15, y: 15 });
  const [direction, setDirection] = useState<Direction>(INITIAL_DIRECTION);
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [gameMode, setGameMode] = useState<GameMode>("walls");
  const [currentGameId, setCurrentGameId] = useState<number | null>(null);
  const [foodEaten, setFoodEaten] = useState(0);
  const [movesCount, setMovesCount] = useState(0);
  const [gameStartTime, setGameStartTime] = useState<Date | null>(null);

  const generateFood = useCallback((): Position => {
    return {
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE),
    };
  }, []);

  const startGameSession = async () => {
    if (isAuthenticated && user && token) {
      try {
        const response = await fetch("/api/games/start", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            user_id: user.id,
            game_mode: gameMode,
          }),
        });

        if (response.ok) {
          const game = await response.json();
          setCurrentGameId(game.id);
          setGameStartTime(new Date());
        }
      } catch (error) {
        console.error("Failed to start game session:", error);
      }
    }
  };

  const endGameSession = async () => {
    if (currentGameId && token && gameStartTime) {
      const duration = Math.floor(
        (new Date().getTime() - gameStartTime.getTime()) / 1000,
      );

      try {
        const response = await fetch(`/api/games/${currentGameId}/end`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            score,
            snake_length: snake.length,
            duration_seconds: duration,
            moves_count: movesCount,
            food_eaten: foodEaten,
            is_completed: true,
          }),
        });

        if (response.ok) {
          const result = await response.json();
          console.log("Game ended:", result.message);
        }
      } catch (error) {
        console.error("Failed to end game session:", error);
      }
    }
  };

  const resetGame = async () => {
    setSnake(INITIAL_SNAKE);
    setFood(generateFood());
    setDirection(INITIAL_DIRECTION);
    setGameOver(false);
    setScore(0);
    setFoodEaten(0);
    setMovesCount(0);
    setIsPlaying(true);
    setCurrentGameId(null);
    setGameStartTime(null);

    // Start new game session
    await startGameSession();
  };

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (!isPlaying) return;

      // Handle pause
      if (e.key === " " || e.key === "Escape") {
        e.preventDefault();
        setIsPaused((prev) => !prev);
        return;
      }

      if (isPaused) return;

      switch (e.key) {
        case "ArrowUp":
        case "w":
        case "W":
          if (direction !== "DOWN") {
            setDirection("UP");
            setMovesCount((m) => m + 1);
          }
          break;
        case "ArrowDown":
        case "s":
        case "S":
          if (direction !== "UP") {
            setDirection("DOWN");
            setMovesCount((m) => m + 1);
          }
          break;
        case "ArrowLeft":
        case "a":
        case "A":
          if (direction !== "RIGHT") {
            setDirection("LEFT");
            setMovesCount((m) => m + 1);
          }
          break;
        case "ArrowRight":
        case "d":
        case "D":
          if (direction !== "LEFT") {
            setDirection("RIGHT");
            setMovesCount((m) => m + 1);
          }
          break;
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [direction, isPlaying, isPaused]);

  useEffect(() => {
    if (!isPlaying || gameOver || isPaused) return;

    const moveSnake = () => {
      setSnake((prevSnake) => {
        const head = prevSnake[0];
        let newHead: Position;

        switch (direction) {
          case "UP":
            newHead = { x: head.x, y: head.y - 1 };
            break;
          case "DOWN":
            newHead = { x: head.x, y: head.y + 1 };
            break;
          case "LEFT":
            newHead = { x: head.x - 1, y: head.y };
            break;
          case "RIGHT":
            newHead = { x: head.x + 1, y: head.y };
            break;
        }

        // Handle wall collision based on game mode
        if (gameMode === "pass-through") {
          // Wrap around the grid
          if (newHead.x < 0) newHead.x = GRID_SIZE - 1;
          if (newHead.x >= GRID_SIZE) newHead.x = 0;
          if (newHead.y < 0) newHead.y = GRID_SIZE - 1;
          if (newHead.y >= GRID_SIZE) newHead.y = 0;
        } else {
          // Walls mode - check for wall collision
          if (
            newHead.x < 0 ||
            newHead.x >= GRID_SIZE ||
            newHead.y < 0 ||
            newHead.y >= GRID_SIZE
          ) {
            setGameOver(true);
            setIsPlaying(false);
            return prevSnake;
          }
        }

        // Check for self-collision
        if (
          prevSnake.some(
            (segment) => segment.x === newHead.x && segment.y === newHead.y,
          )
        ) {
          setGameOver(true);
          setIsPlaying(false);
          // End game session
          endGameSession();
          return prevSnake;
        }

        const newSnake = [newHead, ...prevSnake];

        // Check for food collision
        if (newHead.x === food.x && newHead.y === food.y) {
          setFood(generateFood());
          // Award more points in walls mode (harder)
          const points = gameMode === "walls" ? 15 : 10;
          setScore((s) => s + points);
          setFoodEaten((f) => f + 1);
          return newSnake;
        }

        newSnake.pop();
        return newSnake;
      });
    };

    const interval = setInterval(moveSnake, GAME_SPEED);
    return () => clearInterval(interval);
  }, [direction, food, gameOver, isPlaying, isPaused, gameMode, generateFood]);

  if (isLoading) {
    return (
      <div className="app">
        <h1>Snake Game</h1>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="header">
        <h1>Snake Game</h1>
        <div className="auth-section">
          {isAuthenticated && user ? (
            <div className="user-info">
              <span className="username">👤 {user.username}</span>
              <button onClick={logout} className="logout-button">
                Logout
              </button>
            </div>
          ) : (
            <button
              onClick={() => setShowAuthModal(true)}
              className="login-button"
            >
              Login / Sign Up
            </button>
          )}
        </div>
      </div>

      {showAuthModal && <AuthForms onClose={() => setShowAuthModal(false)} />}

      {!isPlaying && !gameOver && (
        <div className="mode-selection">
          <h3>🎮 Choose Your Game Mode</h3>
          <p className="mode-instruction">
            Click a mode below to select it, then click Start Game
          </p>
          <div className="mode-buttons">
            <button
              className={gameMode === "walls" ? "active" : ""}
              onClick={() => setGameMode("walls")}
            >
              <div className="mode-title">🧱 Walls Mode</div>
              <div className="mode-points">15 points per food</div>
              <div className="mode-desc">Hit a wall = Game Over!</div>
            </button>
            <button
              className={gameMode === "pass-through" ? "active" : ""}
              onClick={() => setGameMode("pass-through")}
            >
              <div className="mode-title">🌀 Pass-Through Mode</div>
              <div className="mode-points">10 points per food</div>
              <div className="mode-desc">Wrap around the edges</div>
            </button>
          </div>
          <div className="mode-details">
            <strong>
              Selected:{" "}
              {gameMode === "walls" ? "🧱 Walls Mode" : "🌀 Pass-Through Mode"}
            </strong>
            <p>
              {gameMode === "walls"
                ? "More challenging! Hitting the wall ends the game. Higher risk, higher reward."
                : "Easier mode! Go off the edge to appear on the opposite side. Perfect for beginners."}
            </p>
          </div>
        </div>
      )}

      <div className="game-info">
        <div className="stat">
          <span className="stat-label">Score:</span>
          <span className="stat-value">{score}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Length:</span>
          <span className="stat-value">{snake.length}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Mode:</span>
          <span className="stat-value current-mode">
            {gameMode === "walls" ? "Walls" : "Pass-Through"}
          </span>
        </div>
      </div>
      {gameOver && <p className="game-over">Game Over!</p>}
      {isPaused && !gameOver && (
        <p className="game-paused">PAUSED - Press SPACE to resume</p>
      )}
      <div
        className="game-board"
        style={{
          width: GRID_SIZE * CELL_SIZE,
          height: GRID_SIZE * CELL_SIZE,
        }}
      >
        {snake.map((segment, index) => (
          <div
            key={index}
            className="snake-segment"
            style={{
              left: segment.x * CELL_SIZE,
              top: segment.y * CELL_SIZE,
              width: CELL_SIZE,
              height: CELL_SIZE,
            }}
          />
        ))}
        <div
          className="food"
          style={{
            left: food.x * CELL_SIZE,
            top: food.y * CELL_SIZE,
            width: CELL_SIZE,
            height: CELL_SIZE,
          }}
        />
      </div>
      <div className="controls">
        {!isPlaying && !gameOver && (
          <button onClick={resetGame} className="start-button">
            Start Game
          </button>
        )}
        {isPlaying && !gameOver && (
          <button
            onClick={() => setIsPaused(!isPaused)}
            className="pause-button"
          >
            {isPaused ? "Resume" : "Pause"}
          </button>
        )}
        {gameOver && <button onClick={resetGame}>Play Again</button>}
      </div>

      {!isPlaying && !gameOver && (
        <div className="controls-help">
          <h3>Controls</h3>
          <div className="control-items">
            <div className="control-item">
              <span className="control-key">↑ ↓ ← →</span>
              <span>or</span>
              <span className="control-key">W A S D</span>
              <span>Move</span>
            </div>
            <div className="control-item">
              <span className="control-key">SPACE</span>
              <span>or</span>
              <span className="control-key">ESC</span>
              <span>Pause</span>
            </div>
          </div>
        </div>
      )}

      <Leaderboard />
    </div>
  );
}

export default App;
