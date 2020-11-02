import keyboard
import time
import copy
import random
from data_management import Data
from colorama import Fore, Back
from os import system


class Menu:
    @staticmethod
    def draw_menu():
        print('''
======================================================================
                            PYTHON GAME                    
      (It's funny because a python is a snake and originally 
      this game is called snake but and I made it with python)
======================================================================
        ''')

    @staticmethod
    def draw_end(points):
        print(f'''
======================================================================
                              GAME OVER! 
                  You made {points} in this game! :o.
======================================================================

                              TOP PLAYERS
                **************************************

{Data.get_top_players()}
                **************************************
''')


class Game:
    def __init__(self, map_size):
        self.map_size = map_size
        self.active = True
        self.points = 0
        self.snake = Snake(map_size)
        self.food_pos = [int(map_size/2 - 3), int(map_size/2)]
        self.map_blueprint = self.create_logic_map()
        self.map_logic = [[]]

    def run(self):
        self.update_logic()
        fps = time.time()
        while self.active:
            time.sleep(0.03)
            if time.time() - fps < 0.1:
                self.check_pressed_key()
                continue

            self.execute_frame()
            self.draw_gfx()
            fps = time.time()

    def draw_gfx(self):
        system("clear")
        cr = Fore.RESET + Back.RESET

        print(f"Points: {self.points}")
        print("=" * (self.map_size * 3 + 2))
        for row in range(self.map_size):
            print("|", end="")
            for col in range(self.map_size):
                if self.map_logic[row][col] == 0: print("  ", end="")
                elif self.map_logic[row][col] == 1: print(Fore.BLUE + Back.LIGHTCYAN_EX + "  ", end=""+cr) # Food for snake
                elif self.map_logic[row][col] == 2: print(Back.LIGHTYELLOW_EX+ "  ", end=""+cr) # Snake head
                elif self.map_logic[row][col] == 3: print(Back.GREEN+"  ", end=""+cr) # Snake body
            print("|")
        print("=" * (self.map_size * 3 + 2))

    def execute_frame(self):
        self.snake.move_player()
        self.update_logic()
        self.check_collision()

    def check_collision(self):
        if self.map_logic[self.snake.y_pos][self.snake.x_pos] == 1:
            self.snake.tail_size += 1
            self.points += 10
            self.food_pos = [random.randrange(0, self.map_size), random.randrange(0, self.map_size)]
        elif self.map_logic[self.snake.y_pos][self.snake.x_pos] == 3:
            self.active = False

    def update_logic(self):
        m = copy.deepcopy(self.map_blueprint)
        m[self.snake.y_pos][self.snake.x_pos] = 2
        for t in self.snake.tail:
            m[int(t[1])][int(t[0])] = 3
        m[self.food_pos[1]][self.food_pos[0]] = 1

        self.map_logic = m

    def create_logic_map(self):
        return [ [ 0 for y in range( self.map_size ) ]
                     for x in range( self.map_size ) ]

    def check_pressed_key(self):
        if self.snake.direction_bk[1] != 0:
            if keyboard.is_pressed("Left"): self.snake.direction = [-1,0]
            elif keyboard.is_pressed("Right"): self.snake.direction = [1, 0]
        elif self.snake.direction_bk[0] != 0:
            if keyboard.is_pressed("Up"): self.snake.direction = [0,-1]
            elif keyboard.is_pressed("Down"): self.snake.direction = [0,1]


class Snake:
    def __init__(self, map_size):
        self.direction = [0,-1]
        self.direction_bk = [0, -1]
        self.x_pos = int(map_size/2)
        self.y_pos = int(map_size/2)
        self.map_size = map_size
        self.reg = [[self.x_pos, self.y_pos]]
        self.tail_size = 1
        self.tail = [[self.x_pos, self.y_pos+1]]

    def move_player(self):
        self.x_pos += self.direction[0]
        self.y_pos += self.direction[1]

        if self.x_pos < 0: self.x_pos = self.map_size-1
        elif self.x_pos > self.map_size-1: self.x_pos = 0
        elif self.y_pos < 0: self.y_pos = self.map_size-1
        elif self.y_pos > self.map_size-1: self.y_pos = 0

        self.tail = self.define_tail()
        self.reg.insert(0, [self.x_pos, self.y_pos])
        if len(self.reg) > self.map_size * self.map_size: self.reg.pop(-1)
        self.direction_bk = self.direction

    def define_tail(self):
        tail = []
        for i in range(self.tail_size):
            tail.append(self.reg[i])

        return tail
