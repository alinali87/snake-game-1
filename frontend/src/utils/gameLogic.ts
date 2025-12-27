/**
 * Game logic utilities for Snake game
 * These pure functions handle game mechanics
 */

export interface Position {
  x: number;
  y: number;
}

export type Direction = "UP" | "DOWN" | "LEFT" | "RIGHT";
export type GameMode = "walls" | "pass-through";

/**
 * Calculate new head position based on direction
 */
export function getNewHeadPosition(
  currentHead: Position,
  direction: Direction
): Position {
  switch (direction) {
    case "UP":
      return { x: currentHead.x, y: currentHead.y - 1 };
    case "DOWN":
      return { x: currentHead.x, y: currentHead.y + 1 };
    case "LEFT":
      return { x: currentHead.x - 1, y: currentHead.y };
    case "RIGHT":
      return { x: currentHead.x + 1, y: currentHead.y };
  }
}

/**
 * Check if position is out of bounds
 */
export function isOutOfBounds(position: Position, gridSize: number): boolean {
  return (
    position.x < 0 ||
    position.x >= gridSize ||
    position.y < 0 ||
    position.y >= gridSize
  );
}

/**
 * Wrap position around grid edges (for pass-through mode)
 */
export function wrapPosition(position: Position, gridSize: number): Position {
  let { x, y } = position;
  
  if (x < 0) x = gridSize - 1;
  if (x >= gridSize) x = 0;
  if (y < 0) y = gridSize - 1;
  if (y >= gridSize) y = 0;
  
  return { x, y };
}

/**
 * Check if snake collides with itself
 */
export function checkSelfCollision(
  head: Position,
  body: Position[]
): boolean {
  return body.some(
    (segment) => segment.x === head.x && segment.y === head.y
  );
}

/**
 * Check if snake head is on food
 */
export function checkFoodCollision(
  head: Position,
  food: Position
): boolean {
  return head.x === food.x && head.y === food.y;
}

/**
 * Calculate score points for eating food based on game mode
 */
export function calculateFoodPoints(gameMode: GameMode): number {
  return gameMode === "walls" ? 15 : 10;
}

/**
 * Check if direction change is valid (can't reverse into self)
 */
export function isValidDirectionChange(
  currentDirection: Direction,
  newDirection: Direction
): boolean {
  const opposites: Record<Direction, Direction> = {
    UP: "DOWN",
    DOWN: "UP",
    LEFT: "RIGHT",
    RIGHT: "LEFT",
  };
  
  return opposites[currentDirection] !== newDirection;
}
