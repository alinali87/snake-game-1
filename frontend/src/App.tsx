import { useState, useEffect, useCallback } from "react";
import "./App.css";

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
  const [snake, setSnake] = useState<Position[]>(INITIAL_SNAKE);
  const [food, setFood] = useState<Position>({ x: 15, y: 15 });
  const [direction, setDirection] = useState<Direction>(INITIAL_DIRECTION);
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [gameMode, setGameMode] = useState<GameMode>("walls");
  const [highScores, setHighScores] = useState<
    Array<{ player_name: string; score: number }>
  >([]);

  const generateFood = useCallback((): Position => {
    return {
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE),
    };
  }, []);

  const resetGame = () => {
    setSnake(INITIAL_SNAKE);
    setFood(generateFood());
    setDirection(INITIAL_DIRECTION);
    setGameOver(false);
    setScore(0);
    setIsPlaying(true);
  };

  const saveScore = async (playerName: string) => {
    try {
      await fetch("/api/scores", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player_name: playerName, score }),
      });
      fetchHighScores();
    } catch (error) {
      console.error("Failed to save score:", error);
    }
  };

  const fetchHighScores = async () => {
    try {
      const response = await fetch("/api/scores");
      const data = await response.json();
      setHighScores(data);
    } catch (error) {
      console.error("Failed to fetch high scores:", error);
    }
  };

  useEffect(() => {
    fetchHighScores();
  }, []);

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
          if (direction !== "DOWN") setDirection("UP");
          break;
        case "ArrowDown":
        case "s":
        case "S":
          if (direction !== "UP") setDirection("DOWN");
          break;
        case "ArrowLeft":
        case "a":
        case "A":
          if (direction !== "RIGHT") setDirection("LEFT");
          break;
        case "ArrowRight":
        case "d":
        case "D":
          if (direction !== "LEFT") setDirection("RIGHT");
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
          return prevSnake;
        }

        const newSnake = [newHead, ...prevSnake];

        // Check for food collision
        if (newHead.x === food.x && newHead.y === food.y) {
          setFood(generateFood());
          // Award more points in walls mode (harder)
          const points = gameMode === "walls" ? 15 : 10;
          setScore((s) => s + points);
          return newSnake;
        }

        newSnake.pop();
        return newSnake;
      });
    };

    const interval = setInterval(moveSnake, GAME_SPEED);
    return () => clearInterval(interval);
  }, [direction, food, gameOver, isPlaying, isPaused, gameMode, generateFood]);

  const handleSaveScore = () => {
    const playerName = prompt("Enter your name:");
    if (playerName) {
      saveScore(playerName);
    }
  };

  return (
    <div className="app">
      <h1>Snake Game</h1>

      {!isPlaying && !gameOver && (
        <div className="mode-selection">
          <h3>Select Game Mode</h3>
          <div className="mode-buttons">
            <button
              className={gameMode === "walls" ? "active" : ""}
              onClick={() => setGameMode("walls")}
            >
              Walls Mode (15 pts/food)
            </button>
            <button
              className={gameMode === "pass-through" ? "active" : ""}
              onClick={() => setGameMode("pass-through")}
            >
              Pass-Through Mode (10 pts/food)
            </button>
          </div>
          <p className="mode-description">
            {gameMode === "walls"
              ? "Hit a wall and game over! More challenging, more points."
              : "Pass through walls and appear on the other side!"}
          </p>
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
        {gameOver && (
          <>
            <button onClick={resetGame}>Play Again</button>
            <button onClick={handleSaveScore}>Save Score</button>
          </>
        )}
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

      <div className="high-scores">
        <h2>High Scores</h2>
        <ol>
          {highScores.map((score, index) => (
            <li key={index}>
              {score.player_name}: {score.score}
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}

export default App;
