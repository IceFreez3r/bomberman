from tkinter import *
import numpy as np
import random

from constants import Sprites

_bombTime = 2000

# Measurements: 
# Grid size: 
# height: 11 cells 
# width: 15 cells
# cell size: cell_size x cell_size


class Bomberman:
    def __init__(self, master, width, height, multiplayer=True):
        self.CELLSIZE = 60
        self.width = width
        self.height = height
        self.master = master
        self.master.title("Bomberman")
        self.master.geometry(f"{self.width * self.CELLSIZE}x{self.height * self.CELLSIZE}")
        self.master.resizable(width=False, height=False)
        self.canvas = Canvas(self.master, width=self.width * self.CELLSIZE, height=self.height * self.CELLSIZE, bg="white")
        self.canvas.pack()
        self.sprites = Sprites(self.CELLSIZE)

        self.time = 0

        # generate game board
        self.bombPositions = []
        self.powerups = []
        self.grid = Grid(self, 15, 11)
        self.multiplayer = multiplayer
        self.characters = []
        for id, pos in enumerate([(0, 0), (self.width - 1, self.height - 1), (self.width - 1, 0), (0, self.height - 1)]):  # corners
            self.characters.append(self.initCharacter(id, pos))

        # bind keys
        self.master.bind("<Up>", lambda event: self.movePlayer(event))
        self.master.bind("<Left>", lambda event: self.movePlayer(event))
        self.master.bind("<Down>", lambda event: self.movePlayer(event))
        self.master.bind("<Right>", lambda event: self.movePlayer(event))
        self.master.bind("w", lambda event: self.movePlayer(event))
        self.master.bind("a", lambda event: self.movePlayer(event))
        self.master.bind("s", lambda event: self.movePlayer(event))
        self.master.bind("d", lambda event: self.movePlayer(event))
        self.master.bind("<space>", lambda event: self.placeBomb(0))
        self.master.bind("<Return>", lambda event: self.placeBomb(1)) # bomb player 1

        # start game
        self.tick(50)

    def initCharacter(self, id, pos):
        '''Initialize a character'''
        character = {}
        character["pos"] = pos
        character["powerups"] = {
            "bomb_range": 2,
            "bomb_amount": 1,
            "throw_bomb": False,
            "kick_bomb": False,
            "movement_speed": 1,  # es nothing
        }
        character["alive"] = True
        character["Label"] = Label(self.canvas, image=self.sprites.PLAYER[id]["DOWN"], width=self.CELLSIZE, height=self.CELLSIZE)
        character["Label"].place(x=character["pos"][0] * self.CELLSIZE, y=character["pos"][1] * self.CELLSIZE)
        return character

    def tick(self, delay):
        self.time += delay
        for bombPos in self.bombPositions:
            if (self.grid.get(*bombPos)["time"] < self.time):
                self.explodeBomb(bombPos)
        # TODO: remove fire
        # TODO: check if there is more than one players left
        self.canvas.after(delay, self.tick, delay)

    def placeBomb(self, characterId):
        '''Place a bomb at the position of the character if possible'''
        charBombs = [1 for bombPos in self.bombPositions if self.grid.get(*bombPos)["owner"] == characterId]
        if self.characters[characterId]["powerups"]["bomb_amount"] <= len(charBombs):
            return
        pos = self.getPosition(characterId)
        bomb = {
            "type": "BOMB",
            "owner": characterId,
            "time": self.time + _bombTime,
            "range": self.characters[characterId]["powerups"]["bomb_range"],
            "Label": Label(self.canvas, image=self.sprites.BOMB, width=self.CELLSIZE, height=self.CELLSIZE),
        }
        bomb["Label"].place(x=self.characters[characterId]["pos"][0] * self.CELLSIZE, y=self.characters[characterId]["pos"][1] * self.CELLSIZE)
        self.grid.board[pos[0]][pos[1]] = bomb
        self.bombPositions.append(pos)
        print(f"Bomb placed at {pos}")

    def explodeBomb(self, pos):
        # Go in all four directions until we hit a indestructible wall
        # or the first destructible wall
        # remove the first destructible wall in each direction (-> chance for powerups)
        # instantly explode all other bombs in the blast
        # remove all players in the blast
        # visual fire effect (kills the player also afterwards)
        bomb = self.grid.get(*pos)
        if bomb["type"] != "BOMB":
            raise Exception("You tried to explode a non-bomb")
        self.bombPositions.remove(pos)
        # remove label
        bomb["Label"].destroy()
        self.grid.board[pos[0]][pos[1]] = {"type": "NONE"}
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            i = 0
            while (i <= bomb["range"] and self.grid.explodePosition(pos[0] + i * direction[0], pos[1] + i * direction[1])):
                for character in self.characters:
                    if character["alive"] and character["pos"] == (pos[0] + i * direction[0], pos[1] + i * direction[1]):
                        self.killCharacter(character)
                i += 1

    def getPosition(self, player):
        '''Get the position of the player'''
        return self.characters[player]["pos"]

    def moveCharacter(self, id, direction):
        '''Move the character'''
        if not self.characters[id]["alive"]:
            return
        # get position
        character = self.characters[id]
        x, y = character["pos"]
        # new position
        if (direction == "UP"):
            y -= 1
        elif (direction == "LEFT"):
            x -= 1
        elif (direction == "DOWN"):
            y += 1
        elif (direction == "RIGHT"):
            x += 1
        # check if position is free
        if self.grid.viableSpot(x, y, character["powerups"]["kick_bomb"]):
            character["pos"] = (x, y)
        # delete old player
        character["Label"].destroy()
        # draw new player
        character["Label"] = Label(self.canvas, image=self.sprites.PLAYER[id][direction], width=self.CELLSIZE, height=self.CELLSIZE)
        character["Label"].place(x=character["pos"][0] * self.CELLSIZE, y=character["pos"][1] * self.CELLSIZE)
        print(f"Player {id} moved to {character['pos']}")
        
    def movePlayer(self, event):
        '''Move the player'''
        print(event)
        # get player
        playerOneMoves = ['w', 'a', 's', 'd']
        playerTwoMoves = ['Up', 'Left', 'Down', 'Right']
        moves = ["UP", "LEFT", "DOWN", "RIGHT"]
        if (event.keysym in playerOneMoves ):
            index = playerOneMoves.index(event.keysym)
            self.moveCharacter(0, moves[index])
        elif (self.multiplayer and event.keysym in playerTwoMoves):
            index = playerTwoMoves.index(event.keysym)
            self.moveCharacter(1, moves[index])

    def killCharacter(self, character):
        '''Kill the character'''
        character["Label"].destroy()
        character["alive"] = False
        print(f"Player {self.characters.index(character)} died")

##### Gedanken zur board matrix:
## board hat verschiedene cellen: jede Zelle bekommt ein dict
## @case1 IMMUNE wall (label)
## @case2 BREAKABLE wall (label)
## @case2 bomb (time, power, owner, label)

class Grid:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.board = np.full((width, height), {"type": "NONE"})
        self.draw()

    def draw(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = {}
                if x % 2 != 0 and y % 2 != 0:
                    cell["type"] = "IMMUNE_WALL"
                    cell["Label"] = Label(self.game.canvas, image=self.game.sprites.WALL["IMMUNE"], width=self.game.CELLSIZE, height=self.game.CELLSIZE)
                elif 1 < x < self.width - 2 or 1 < y < self.height - 2:
                    if random.random() < 0.2:
                        continue
                    cell["type"] = "BREAKABLE_WALL"
                    cell["Label"] = Label(self.game.canvas, image=self.game.sprites.WALL["BREAKABLE"], width=self.game.CELLSIZE, height=self.game.CELLSIZE)
                else:
                    continue
                cell["Label"].place(x=x * self.game.CELLSIZE, y=y * self.game.CELLSIZE)
                self.board[x][y] = cell

    def viableSpot(self, x, y, pushBombs = False):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        if not pushBombs:
            return self.board[x][y]["type"] == "NONE" or self.board[x][y]["type"] == "POWERUP" or self.board[x][y]["type"] == "FIRE"
        else:
            # push bomb here?
            return self.board[x][y]["type"] == "NONE" or self.board[x][y]["type"] == "BOMB"

    def explodePosition(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        elif self.board[x][y]["type"] == "IMMUNE_WALL":
            return False
        continueExplode = True
        if self.board[x][y]["type"] == "BREAKABLE_WALL":
            self.board[x][y]["Label"].destroy()
            self.board[x][y]["type"] = "NONE"
            print(f"Wall at {x}, {y} destroyed")
            # TODO: spawn powerup
            continueExplode = False
        elif self.board[x][y]["type"] == "BOMB":
            self.game.explodeBomb((x, y))
        self.burnPosition(x, y)
        return continueExplode

    def burnPosition(self, x, y):
        if self.board[x][y]["type"] == "FIRE":
            self.board[x][y]["time"] = self.game.time + 1000
        else:
            if "Label" in self.board[x][y]:
                self.board[x][y]["Label"].destroy()
            self.board[x][y] = {
                "type": "FIRE",
                "Label": Label(self.game.canvas, image=self.game.sprites.FIRE, width=self.game.CELLSIZE, height=self.game.CELLSIZE),
                "time": self.game.time + 1000
            }
            self.board[x][y]["Label"].place(x=x * self.game.CELLSIZE, y=y * self.game.CELLSIZE)

    def get(self, x, y):
        return self.board[x][y]

window = Tk()
bomb = Bomberman(window, 15, 11)
window.mainloop()
