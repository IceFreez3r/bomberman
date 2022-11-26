from tkinter import *
from PIL import Image, ImageTk


def resized_image(path, width, height):
    image = Image.open(path)
    image = image.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


class Sprites:
    def __init__(self, cell_size=80):
        self.BOMB = resized_image("Sprites/Bomb/Bomb_f01.png", width=cell_size, height=cell_size)
        self.WALL = {
            "IMMUNE": resized_image("Sprites/Blocks/SolidBlock.png", width=cell_size, height=cell_size),
            "BREAKABLE": resized_image("Sprites/Blocks/ExplodableBlock.png", width=cell_size, height=cell_size),
        }
        self.PLAYER = {
            0: {
                "UP": resized_image("Sprites/Bomberman/0/Up.png", width=cell_size, height=cell_size),
                "DOWN": resized_image("Sprites/Bomberman/0/Down.png", width=cell_size, height=cell_size),
                "RIGHT": resized_image("Sprites/Bomberman/0/Right.png", width=cell_size, height=cell_size),
                "LEFT": resized_image("Sprites/Bomberman/0/Left.png", width=cell_size, height=cell_size),
            },
            1: {
                "UP": resized_image("Sprites/Bomberman/1/Up.png", width=cell_size, height=cell_size),
                "DOWN": resized_image("Sprites/Bomberman/1/Down.png", width=cell_size, height=cell_size),
                "RIGHT": resized_image("Sprites/Bomberman/1/Right.png", width=cell_size, height=cell_size),
                "LEFT": resized_image("Sprites/Bomberman/1/Left.png", width=cell_size, height=cell_size),
            },
            2: {
                "UP": resized_image("Sprites/Bomberman/2/Up.png", width=cell_size, height=cell_size),
                "DOWN": resized_image("Sprites/Bomberman/2/Down.png", width=cell_size, height=cell_size),
                "RIGHT": resized_image("Sprites/Bomberman/2/Right.png", width=cell_size, height=cell_size),
                "LEFT": resized_image("Sprites/Bomberman/2/Left.png", width=cell_size, height=cell_size),
            },
            3: {
                "UP": resized_image("Sprites/Bomberman/3/Up.png", width=cell_size, height=cell_size),
                "DOWN": resized_image("Sprites/Bomberman/3/Down.png", width=cell_size, height=cell_size),
                "RIGHT": resized_image("Sprites/Bomberman/3/Right.png", width=cell_size, height=cell_size),
                "LEFT": resized_image("Sprites/Bomberman/3/Left.png", width=cell_size, height=cell_size),
            },
        }
        self.FIRE = resized_image("Sprites/Flame/Flame_f00.png", width=cell_size, height=cell_size)
