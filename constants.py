from tkinter import *
from PIL import Image, ImageTk
from enum import Enum


class Sprites:
    def __init__(self, cellSize=80):
        self.BOMB = self.resizedImage("Sprites/Bomb/Bomb_f01.png", width=cellSize, height=cellSize)
        self.WALL = {
            WallType.IMMUNE: self.resizedImage("Sprites/Blocks/SolidBlock.png", width=cellSize, height=cellSize),
            WallType.BREAKABLE: self.resizedImage("Sprites/Blocks/ExplodableBlock.png", width=cellSize, height=cellSize),
        }
        self.PLAYER = {
            0: {
                Direction.UP: self.resizedImage("Sprites/Bomberman/0/Up.png", width=cellSize, height=cellSize),
                Direction.DOWN: self.resizedImage("Sprites/Bomberman/0/Down.png", width=cellSize, height=cellSize),
                Direction.RIGHT: self.resizedImage("Sprites/Bomberman/0/Right.png", width=cellSize, height=cellSize),
                Direction.LEFT: self.resizedImage("Sprites/Bomberman/0/Left.png", width=cellSize, height=cellSize),
            },
            1: {
                Direction.UP: self.resizedImage("Sprites/Bomberman/1/Up.png", width=cellSize, height=cellSize),
                Direction.DOWN: self.resizedImage("Sprites/Bomberman/1/Down.png", width=cellSize, height=cellSize),
                Direction.RIGHT: self.resizedImage("Sprites/Bomberman/1/Right.png", width=cellSize, height=cellSize),
                Direction.LEFT: self.resizedImage("Sprites/Bomberman/1/Left.png", width=cellSize, height=cellSize),
            },
            2: {
                Direction.UP: self.resizedImage("Sprites/Bomberman/2/Up.png", width=cellSize, height=cellSize),
                Direction.DOWN: self.resizedImage("Sprites/Bomberman/2/Down.png", width=cellSize, height=cellSize),
                Direction.RIGHT: self.resizedImage("Sprites/Bomberman/2/Right.png", width=cellSize, height=cellSize),
                Direction.LEFT: self.resizedImage("Sprites/Bomberman/2/Left.png", width=cellSize, height=cellSize),
            },
            3: {
                Direction.UP: self.resizedImage("Sprites/Bomberman/3/Up.png", width=cellSize, height=cellSize),
                Direction.DOWN: self.resizedImage("Sprites/Bomberman/3/Down.png", width=cellSize, height=cellSize),
                Direction.RIGHT: self.resizedImage("Sprites/Bomberman/3/Right.png", width=cellSize, height=cellSize),
                Direction.LEFT: self.resizedImage("Sprites/Bomberman/3/Left.png", width=cellSize, height=cellSize),
            },
        }
        self.FIRE = self.resizedImage("Sprites/Flame/Flame_f00.png", width=cellSize, height=cellSize)
        self.POWERUPS = {
            Powerup.BOMB_AMOUNT: self.resizedImage("Sprites/Powerups/BombPowerup.png", width=cellSize, height=cellSize),
            Powerup.BOMB_RANGE: self.resizedImage("Sprites/Powerups/FlamePowerup.png", width=cellSize, height=cellSize),
            Powerup.THROW_BOMB: self.resizedImage("Sprites/title_flat.jpg", width=cellSize, height=cellSize),
            Powerup.KICK_BOMB: self.resizedImage("Sprites/title_flat.jpg", width=cellSize, height=cellSize),
            Powerup.MOVEMENT_SPEED: self.resizedImage("Sprites/Powerups/SpeedPowerup.png", width=cellSize, height=cellSize),
        }

    def resizedImage(self, path, width, height):
        image = Image.open(path)
        image = image.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)

class Config:
    def __init__(self):
        self.CELL_SIZE = 60
        self.BOMBTIME = 3000
        self.FIRETIME = 1500
        self.INIT_POWERUPS = {
            Powerup.BOMB_AMOUNT: 1,
            Powerup.BOMB_RANGE: 2,
            Powerup.THROW_BOMB: 1,
            Powerup.KICK_BOMB: True,
            Powerup.MOVEMENT_SPEED: 1,
        }
        self.LIFES = 1
        self.WALL_CHANCE = 0.7
        self.WIDTH = 15
        self.HEIGHT = 11

class Coordinate:
    def __init__(self, x, y) -> None:
        self.coords = (x, y)
        self.max_x = Config().WIDTH
        self.max_y = Config().HEIGHT

    def __add__(self, other) -> "Coordinate":
        x1, y1 = self.coords
        x2, y2 = other.coords
        return Coordinate((x1 + x2) % self.max_x, (y1 + y2) % self.max_y)

    def __mul__(self, scalar) -> "Coordinate":
        x, y = self.coords
        return Coordinate((x * scalar) % self.max_x, (y * scalar) % self.max_y)

    def __eq__(self, __o: object) -> bool:
        return self.coords == __o.coords

    def __getitem__(self, key):
        return self.coords[key]

    def get(self):
        return self.coords

class Powerup(Enum):
    BOMB_AMOUNT = 0
    BOMB_RANGE = 1
    THROW_BOMB = 2
    KICK_BOMB = 3
    MOVEMENT_SPEED = 4

class Direction(Enum):
    UP = Coordinate(0, -1)
    RIGHT = Coordinate(1, 0)
    DOWN = Coordinate(0, 1)
    LEFT = Coordinate(-1, 0)

class WallType(Enum):
    IMMUNE = 0
    BREAKABLE = 1
