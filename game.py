import copy
from tkinter import *
import numpy as np
import random
from constants import Sprites, Config, Direction, Coordinate, WallType, Powerup


class Bomberman:
    def __init__(self, master, multiplayer=True):
        self.config = Config()
        self.width = self.config.WIDTH
        self.height = self.config.HEIGHT
        self.master = master
        self.master.title("Bomberman")
        self.master.geometry(f"{self.width * self.config.CELL_SIZE}x{self.height * self.config.CELL_SIZE}")
        self.master.resizable(width=False, height=False)
        self.canvas = Canvas(self.master, width=self.width * self.config.CELL_SIZE, height=self.height * self.config.CELL_SIZE, bg="white")
        self.canvas.pack()
        self.sprites = Sprites(self.config.CELL_SIZE)

        # generate game board
        self.powerups = np.empty((self.width, self.height), dtype=object) # coming soon
        self.fires = np.empty((self.width, self.height), dtype=object)
        self.bombs = np.empty((self.width, self.height), dtype=object)
        self.immune_walls = np.full((self.width, self.height), False)
        self.breakable_walls = np.empty((self.width, self.height), dtype=object)
        self.init_grid()

        self.multiplayer = multiplayer
        self.characters = [self.init_character(id, pos) for id, pos in enumerate(self.get_corners())]

        self.bind_input()

        self.time = 0
        # start game
        self.tick(50)

    def init_character(self, id, pos):
        '''Returns a fresh character'''
        character = {
            "id": id,
            "pos" : pos,
            "powerups": copy.copy(self.config.INIT_POWERUPS),
            "lifes": self.config.LIFES,
            "direction": Direction.DOWN,
            "Label": self.cell_label(self.sprites.PLAYER[id][Direction.DOWN], pos),
        }
        return character

    def init_grid(self):
        '''
        ###########
        # xxxxxxx #
        #x#x#x#x#x#
        #xxxxxxxxx#
        #x#x#x#x#x#
        # xxxxxxx #
        ###########
        '''
        for x, y in np.ndindex(self.powerups.shape):
            if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                self.place_immune_wall(Coordinate(x, y))
            elif x % 2 == 0 and y % 2 == 0:
                self.place_immune_wall(Coordinate(x, y))
            elif (2 < x < self.width - 3 or 2 < y < self.height - 3) and random.random() < self.config.WALL_CHANCE:
                self.place_breakable_wall(Coordinate(x, y))

    def bind_input(self):
        self.master.bind("w", lambda event: self.move_character(0, Direction.UP))
        self.master.bind("a", lambda event: self.move_character(0, Direction.LEFT))
        self.master.bind("s", lambda event: self.move_character(0, Direction.DOWN))
        self.master.bind("d", lambda event: self.move_character(0, Direction.RIGHT))
        self.master.bind("<space>", lambda event: self.place_bomb(0))
        if self.multiplayer:
            self.master.bind("<Up>", lambda event: self.move_character(1, Direction.UP))
            self.master.bind("<Left>", lambda event: self.move_character(1, Direction.LEFT))
            self.master.bind("<Down>", lambda event: self.move_character(1, Direction.DOWN))
            self.master.bind("<Right>", lambda event: self.move_character(1, Direction.RIGHT))
            self.master.bind("<Return>", lambda event: self.place_bomb(1))

    def tick(self, delay):
        self.time += delay
        for index in np.ndindex(self.width, self.height):
            if self.fires[index] and self.fires[index]["time"] < self.time:
                self.remove_fire(Coordinate(*index))
            if self.bombs[index] and self.bombs[index]["time"] < self.time:
                self.remove_bomb(Coordinate(*index))

        alive_characters = [characters for characters in self.characters if characters["lifes"]]
        if len(alive_characters) < 2:
            self.end_game(alive_characters)

        self.canvas.after(delay, self.tick, delay)

    def end_game(self, alive_characters):
        if len(alive_characters) == 1:
            print(f"Character {alive_characters[0]['id']} won the game!")
        else:
            print("Everyone is dead x.x")
        # self.master.close() # correct name isn't `closed`

    def place_immune_wall(self, pos):
        immune_wall = {
            "Label": self.cell_label(self.sprites.WALL[WallType.IMMUNE], pos),
        }
        self.immune_walls[pos.get()] = immune_wall

    def remove_immune_wall(self, pos):
        raise Exception("Immune walls are .. immune")

    def place_breakable_wall(self, pos):
        breakable_wall = {
            "Label": self.cell_label(self.sprites.WALL[WallType.BREAKABLE], pos),
        }
        self.breakable_walls[pos.get()] = breakable_wall

    def remove_breakable_wall(self, pos):
        if random.random() < 0.3:
            self.place_powerup(pos)
        self.clear_position(self.breakable_walls, pos)

    def place_bomb(self, character_id, pos = None, bomb_timer = None):
        '''Place a bomb at the position of the character if possible'''
        character = self.characters[character_id]
        if not character["lifes"]:
            return
        # check if there is already a bomb at the current position
        pos = pos if pos else self.get_character_position(character_id)
        if self.bombs[pos.get()]:
            self.throw_bomb(character_id, pos)
        else:
            charBombs = [1 for bomb in self.bombs.flatten() if bomb and bomb["owner"] == character_id]
            if character["powerups"][Powerup.BOMB_AMOUNT] == len(charBombs):
                return

            bomb_time = self.time + self.config.BOMBTIME if bomb_timer is None else bomb_timer
            bomb = {
                "owner": character_id,
                "time": bomb_time,
                "range": character["powerups"][Powerup.BOMB_RANGE],
                "Label": self.cell_label(self.sprites.BOMB, pos),
            }
            self.bombs[pos.get()] = bomb
            print(f"Bomb placed at {pos.get()}")

    def remove_bomb(self, pos):
        # Go in all four directions until we hit a indestructible wall
        # or the first destructible wall
        # remove the first destructible wall in each direction (-> chance for powerups)
        # instantly explode all other bombs in the blast
        # remove all players in the blast
        # visual fire effect (kills the player also afterwards)
        bomb = self.bombs[pos.get()]
        self.clear_position(self.bombs, pos)
        for direction in [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]:
            for i in range(bomb["range"] + 1):
                new_pos = pos + direction.value * i
                x, y = new_pos.get()
                if not (0 <= x < self.width and 0 <= y < self.height):
                    break
                if self.immune_walls[new_pos.get()]:
                    break
                if self.breakable_walls[new_pos.get()]:
                    self.place_fire(new_pos)
                    self.remove_breakable_wall(new_pos)
                    break
                if self.bombs[new_pos.get()]:
                    self.remove_bomb(new_pos)
                for character in self.characters:
                    if character["pos"] == new_pos:
                        self.damage_character(character)
                self.place_fire(new_pos)

    def place_fire(self, pos):
        if self.fires[pos.get()]:
            # renew existing fire
            self.fires[pos.get()]["time"] = self.time + self.config.FIRETIME
        else:
            fire = {
                "time": self.time + self.config.FIRETIME,
                "Label": self.cell_label(self.sprites.FIRE, pos),
            }
            self.fires[pos.get()] = fire

    def remove_fire(self, pos):
        self.clear_position(self.fires, pos)

    def place_powerup(self, pos):
        type = random.choice(list(Powerup))
        label = self.sprites.POWERUPS[type]
        powerup = {
            "Label": self.cell_label(label, pos),
            "type": type,
        }
        self.powerups[pos.get()] = powerup

    def remove_powerup(self, pos):
        self.clear_position(self.powerups, pos)

    def clear_position(self, matrix, pos):
        matrix[pos.get()]["Label"].destroy()
        matrix[pos.get()] = None

    def get_character_position(self, character_id):
        return self.characters[character_id]["pos"]

    # @check_alive # TODO
    def move_character(self, character_id, direction):
        '''Move the character'''
        if not self.characters[character_id]["lifes"]:
            return
        character = self.characters[character_id]
        character["direction"] = direction
        new_pos = character["pos"] + direction.value
        pos = character["pos"]
        if self.can_walk_to_spot(new_pos, character["powerups"][Powerup.KICK_BOMB]):
            pos = new_pos
        character["pos"] = pos
        character["Label"].destroy()
        character["Label"] = self.cell_label(self.sprites.PLAYER[character_id][direction], character["pos"])
        if self.fires[pos.get()]:
            self.damage_character(character)
        if self.powerups[pos.get()]:
            self.pickup_powerup(character_id, pos)
        if self.bombs[pos.get()]:
            self.kick_bomb(character_id, pos, direction)
        print(f"Player {character_id} moved to {character['pos'].get()}")

    def damage_character(self, character):
        '''Removes one life and kills the character if no lifes are left'''
        character["lifes"] -= 1
        if character["lifes"] == 0:
            character["Label"].destroy()
            character["pos"] = Coordinate(-1, -1)
            print(f"Character {self.characters.index(character)} died")
        else:
            print(f"Character {self.characters.index(character)} has {character['lifes']} lifes left")

    def pickup_powerup(self, character_id, pos):
        powerup_type = self.powerups[pos.get()]["type"]
        if powerup_type == Powerup.BOMB_AMOUNT:
            self.characters[character_id]["powerups"][Powerup.BOMB_AMOUNT] += 1
        elif powerup_type == Powerup.BOMB_RANGE:
            self.characters[character_id]["powerups"][Powerup.BOMB_RANGE] += 1
        elif powerup_type == Powerup.THROW_BOMB:
            self.characters[character_id]["powerups"][Powerup.THROW_BOMB] = True
        elif powerup_type == Powerup.KICK_BOMB:
            self.characters[character_id]["powerups"][Powerup.KICK_BOMB] = True
        elif powerup_type == Powerup.MOVEMENT_SPEED:
            new_movement_speed = self.characters[character_id]["powerups"][Powerup.MOVEMENT_SPEED] + 1
            self.characters[character_id]["powerups"][Powerup.MOVEMENT_SPEED] = min(3, new_movement_speed)
        self.remove_powerup(pos)

    def throw_bomb(self, character_id, pos):
        '''Throw a bomb in the given direction'''
        character = self.characters[character_id]
        allowed_free_spots = character["powerups"][Powerup.THROW_BOMB]
        if allowed_free_spots == 0:
            return

        direction = character["direction"]
        self.clear_position(self.bombs, pos)
        while allowed_free_spots > 0:
            pos = pos + direction.value
            if not self.is_wall_or_bomb(pos):
                allowed_free_spots -= 1
        self.place_bomb(character_id, pos) # We could add bomb time here as in kick_bomb

    def kick_bomb(self, character_id, pos, direction):
        '''Kick a bomb in the given direction'''
        character = self.characters[character_id]
        if not character["powerups"][Powerup.KICK_BOMB]:
            return
        cur_bomb_time = self.bombs[pos.get()]["time"]

        self.clear_position(self.bombs, pos)
        while not self.is_wall_or_bomb(pos + direction.value):
            pos = pos + direction.value
        self.place_bomb(character_id, pos, cur_bomb_time)

    def get_corners(self):
        return [Coordinate(1, 1),
                Coordinate(self.width - 2, self.height - 2),
                Coordinate(self.width - 2, 1),
                Coordinate(1, self.height - 2)]

    def can_walk_to_spot(self, pos, kick_bombs = False):
        x, y = pos.get()
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return not self.immune_walls[pos.get()] and\
               not self.breakable_walls[pos.get()] and\
               (not self.bombs[pos.get()] or kick_bombs)

    def is_wall_or_bomb(self, pos):
        return self.immune_walls[pos.get()] or self.breakable_walls[pos.get()] or self.bombs[pos.get()]

    def cell_label(self, image, pos):
        label = Label(self.canvas, image=image, width=self.config.CELL_SIZE, height=self.config.CELL_SIZE)
        label.place(x=pos[0] * self.config.CELL_SIZE, y=pos[1] * self.config.CELL_SIZE)
        return label

window = Tk()
bomberman = Bomberman(window)
window.mainloop()
