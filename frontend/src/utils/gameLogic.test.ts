import { describe, it, expect } from 'vitest'
import {
  getNewHeadPosition,
  isOutOfBounds,
  wrapPosition,
  checkSelfCollision,
  checkFoodCollision,
  calculateFoodPoints,
  isValidDirectionChange,
  type Position,
} from './gameLogic'

describe('getNewHeadPosition', () => {
  it('moves up correctly', () => {
    const head: Position = { x: 5, y: 5 }
    const newHead = getNewHeadPosition(head, 'UP')
    expect(newHead).toEqual({ x: 5, y: 4 })
  })

  it('moves down correctly', () => {
    const head: Position = { x: 5, y: 5 }
    const newHead = getNewHeadPosition(head, 'DOWN')
    expect(newHead).toEqual({ x: 5, y: 6 })
  })

  it('moves left correctly', () => {
    const head: Position = { x: 5, y: 5 }
    const newHead = getNewHeadPosition(head, 'LEFT')
    expect(newHead).toEqual({ x: 4, y: 5 })
  })

  it('moves right correctly', () => {
    const head: Position = { x: 5, y: 5 }
    const newHead = getNewHeadPosition(head, 'RIGHT')
    expect(newHead).toEqual({ x: 6, y: 5 })
  })
})

describe('isOutOfBounds', () => {
  const gridSize = 20

  it('detects position outside left boundary', () => {
    expect(isOutOfBounds({ x: -1, y: 10 }, gridSize)).toBe(true)
  })

  it('detects position outside right boundary', () => {
    expect(isOutOfBounds({ x: 20, y: 10 }, gridSize)).toBe(true)
  })

  it('detects position outside top boundary', () => {
    expect(isOutOfBounds({ x: 10, y: -1 }, gridSize)).toBe(true)
  })

  it('detects position outside bottom boundary', () => {
    expect(isOutOfBounds({ x: 10, y: 20 }, gridSize)).toBe(true)
  })

  it('returns false for valid position', () => {
    expect(isOutOfBounds({ x: 10, y: 10 }, gridSize)).toBe(false)
  })

  it('returns false for edge positions', () => {
    expect(isOutOfBounds({ x: 0, y: 0 }, gridSize)).toBe(false)
    expect(isOutOfBounds({ x: 19, y: 19 }, gridSize)).toBe(false)
  })
})

describe('wrapPosition', () => {
  const gridSize = 20

  it('wraps left edge to right', () => {
    const wrapped = wrapPosition({ x: -1, y: 10 }, gridSize)
    expect(wrapped).toEqual({ x: 19, y: 10 })
  })

  it('wraps right edge to left', () => {
    const wrapped = wrapPosition({ x: 20, y: 10 }, gridSize)
    expect(wrapped).toEqual({ x: 0, y: 10 })
  })

  it('wraps top edge to bottom', () => {
    const wrapped = wrapPosition({ x: 10, y: -1 }, gridSize)
    expect(wrapped).toEqual({ x: 10, y: 19 })
  })

  it('wraps bottom edge to top', () => {
    const wrapped = wrapPosition({ x: 10, y: 20 }, gridSize)
    expect(wrapped).toEqual({ x: 10, y: 0 })
  })

  it('does not modify valid positions', () => {
    const wrapped = wrapPosition({ x: 10, y: 10 }, gridSize)
    expect(wrapped).toEqual({ x: 10, y: 10 })
  })
})

describe('checkSelfCollision', () => {
  it('detects collision with body', () => {
    const head: Position = { x: 5, y: 5 }
    const body: Position[] = [
      { x: 4, y: 5 },
      { x: 5, y: 5 },  // Collision here
      { x: 6, y: 5 },
    ]
    expect(checkSelfCollision(head, body)).toBe(true)
  })

  it('returns false when no collision', () => {
    const head: Position = { x: 5, y: 5 }
    const body: Position[] = [
      { x: 4, y: 5 },
      { x: 3, y: 5 },
      { x: 2, y: 5 },
    ]
    expect(checkSelfCollision(head, body)).toBe(false)
  })

  it('returns false for empty body', () => {
    const head: Position = { x: 5, y: 5 }
    expect(checkSelfCollision(head, [])).toBe(false)
  })
})

describe('checkFoodCollision', () => {
  it('detects when snake eats food', () => {
    const head: Position = { x: 10, y: 10 }
    const food: Position = { x: 10, y: 10 }
    expect(checkFoodCollision(head, food)).toBe(true)
  })

  it('returns false when snake misses food', () => {
    const head: Position = { x: 10, y: 10 }
    const food: Position = { x: 11, y: 10 }
    expect(checkFoodCollision(head, food)).toBe(false)
  })
})

describe('calculateFoodPoints', () => {
  it('returns 15 points for walls mode', () => {
    expect(calculateFoodPoints('walls')).toBe(15)
  })

  it('returns 10 points for pass-through mode', () => {
    expect(calculateFoodPoints('pass-through')).toBe(10)
  })
})

describe('isValidDirectionChange', () => {
  it('allows perpendicular direction changes', () => {
    expect(isValidDirectionChange('UP', 'LEFT')).toBe(true)
    expect(isValidDirectionChange('UP', 'RIGHT')).toBe(true)
    expect(isValidDirectionChange('LEFT', 'UP')).toBe(true)
    expect(isValidDirectionChange('LEFT', 'DOWN')).toBe(true)
  })

  it('prevents reversing direction', () => {
    expect(isValidDirectionChange('UP', 'DOWN')).toBe(false)
    expect(isValidDirectionChange('DOWN', 'UP')).toBe(false)
    expect(isValidDirectionChange('LEFT', 'RIGHT')).toBe(false)
    expect(isValidDirectionChange('RIGHT', 'LEFT')).toBe(false)
  })

  it('allows continuing in same direction', () => {
    expect(isValidDirectionChange('UP', 'UP')).toBe(true)
    expect(isValidDirectionChange('DOWN', 'DOWN')).toBe(true)
    expect(isValidDirectionChange('LEFT', 'LEFT')).toBe(true)
    expect(isValidDirectionChange('RIGHT', 'RIGHT')).toBe(true)
  })
})
