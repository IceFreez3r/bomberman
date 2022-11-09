from tkinter import *
from PIL import Image, ImageTk

class Sprites:
    def __init__(self, cellSize=80):
        self.BOMB = self.resizedImage("Sprites/Bomb/Bomb_f01.png", width=cellSize, height=cellSize)
        self.WALL = {
            "IMMUNE": self.resizedImage("Sprites/Blocks/SolidBlock.png", width=cellSize, height=cellSize),
            "BREAKABLE": self.resizedImage("Sprites/Blocks/ExplodableBlock.png", width=cellSize, height=cellSize),
        }
        self.PLAYER = {
            0: {
                "UP": self.resizedImage("Sprites/Bomberman/0/Up.png", width=cellSize, height=cellSize),
                "DOWN": self.resizedImage("Sprites/Bomberman/0/Down.png", width=cellSize, height=cellSize),
                "RIGHT": self.resizedImage("Sprites/Bomberman/0/Right.png", width=cellSize, height=cellSize),
                "LEFT": self.resizedImage("Sprites/Bomberman/0/Left.png", width=cellSize, height=cellSize),
            },
            1: {
                "UP": self.resizedImage("Sprites/Bomberman/1/Up.png", width=cellSize, height=cellSize),
                "DOWN": self.resizedImage("Sprites/Bomberman/1/Down.png", width=cellSize, height=cellSize),
                "RIGHT": self.resizedImage("Sprites/Bomberman/1/Right.png", width=cellSize, height=cellSize),
                "LEFT": self.resizedImage("Sprites/Bomberman/1/Left.png", width=cellSize, height=cellSize),
            },
            2: {
                "UP": self.resizedImage("Sprites/Bomberman/2/Up.png", width=cellSize, height=cellSize),
                "DOWN": self.resizedImage("Sprites/Bomberman/2/Down.png", width=cellSize, height=cellSize),
                "RIGHT": self.resizedImage("Sprites/Bomberman/2/Right.png", width=cellSize, height=cellSize),
                "LEFT": self.resizedImage("Sprites/Bomberman/2/Left.png", width=cellSize, height=cellSize),
            },
            3: {
                "UP": self.resizedImage("Sprites/Bomberman/3/Up.png", width=cellSize, height=cellSize),
                "DOWN": self.resizedImage("Sprites/Bomberman/3/Down.png", width=cellSize, height=cellSize),
                "RIGHT": self.resizedImage("Sprites/Bomberman/3/Right.png", width=cellSize, height=cellSize),
                "LEFT": self.resizedImage("Sprites/Bomberman/3/Left.png", width=cellSize, height=cellSize),
            },
        }
        self.FIRE = self.resizedImage("Sprites/Flame/Flame_f00.png", width=cellSize, height=cellSize)

    def resizedImage(self, path, width, height):
        image = Image.open(path)
        image = image.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)
