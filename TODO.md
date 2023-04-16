## Current State

- Grid is build with unbreakable and immune walls
- Players are movable
- Bombs are set to the position
- function destroying walls
- Bombs are limited (1 per default)
- bomb explodable
- bomb removable
- powerups
- kick bombs
- throw bombs

## Functionality
- Wrapping Game Menu
    - Settings
        - Number of Players
        - Number of Lives
        - Number of Bombs
        - Bomb Range
        - Speed
        - Powerups
            - Bomb Power
            - Bomb Limit
            - Speed
            - Bomb Kick
            - Bomb Throw
    - Start Game -> Start game.py
    - Game Over Screen

### Powerups

- bomb power
- bomb limit
- speed
- bomb kick
- bomb throw

## Art

- add transparency to images
- floor for walkable fields (background)
- background (no white background of boombs)
- gameboard (number of lifes per player)

## Enemies

- KI for NPCs

## Notes

tick function necessary? could just use `after()` in placeBomb/placeFire
prefilled `Label()` + `place()` function
    canvas, width, height and x, y are always the same for cell images
