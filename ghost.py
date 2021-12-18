from abc import ABC, abstractmethod
import pygame
import math as m
import random
from constant import *
from pyswip import Prolog

class Ghost(ABC):
    def __init__(self, position, game, pac):
        self.pac = pac
        self.game = game
        self.grid_pos = position
        self.pic_pos = self.get_pic_pos()
        self.mode = 'scatter'
        self.direction = Vector2(0,-1)
        self.dec_point = self.game.ghost_dec
        self.wall_pos = self.game.walls
        self.target = None
        self.in_home = 1
        self.last_dec_point = None
        self.start_mode = pygame.time.get_ticks()
        self.speed = 2
        self.home_en = self.game.ghost_en
        self.prolog = Prolog()
        self.prolog.consult('ghost_ai.pl')
        self.chase_count = 0
        if self.game.win_streak == 0:
            self.scatter_limit = 7
            self.chase_limit = 20
            self.frighten_limit = 10
        elif self.game.win_streak < 3:
            self.scatter_limit = 5
            self.chase_limit = 25
            self.frighten_limit = 7
        else:
            self.scatter_limit = 5
            self.chase_limit = 35
            self.frighten_limit = 5
        self.find_target()

    ''' get drawing position from grid position '''
    def get_pic_pos(self):
        return Vector2((self.grid_pos[0] * GRID_SIZE) - 5, (self.grid_pos[1] * GRID_SIZE) - 5)

    ''' find distance between two coordinates '''
    def find_distance(self, start, end):
        return m.sqrt ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

    ''' check that next grid is a wall or not '''
    def movable(self):
        for wall in self.wall_pos:
            if self.grid_pos + self.direction == wall:
                self.direction = self.find_turn()
                return False
        return True

    ''' find the next way to move '''
    def find_turn(self):
        turns = [Vector2(0,-1), Vector2(-1,0), Vector2(0,1), Vector2(1,0)]
        turns.remove(self.direction)

        if self.direction == [0,1]:
            turns.remove([0,-1])
        elif self.direction == [0,-1]:
            turns.remove([0,1])
        elif self.direction == [1,0]:
            turns.remove([-1,0])
        elif self.direction == [-1,0]:
            turns.remove([1,0])

        for d in turns:
            for wall in self.wall_pos:
                if self.grid_pos + d == wall:
                    turns.remove(d)
        return turns[0]

    ''' make ghost turn into the fastest direction to the target '''
    def make_decision(self):
        if self.mode == 'frighten':
            self.direction = random.choice([Vector2(0,-1), Vector2(-1,0), Vector2(0,1), Vector2(1,0)])
        elif self.in_home != 1:

            g_node = "node({}, {})".format(int(self.grid_pos.x), int(self.grid_pos.y))
            pac_pos = "node({}, {})".format(int(self.target.x), int(self.target.y))

            result = list(self.prolog.query("findTurn({}, {}, {}, Turn)".format(g_node, pac_pos, getVector(self.direction))))[0]["Turn"]
            self.direction = DIRECTIONTOVECTOR[result]


    def update(self):
        timer = (pygame.time.get_ticks() - self.start_mode) / 1000

        ''' change ghost states '''
        if self.mode == 'scatter':
            if timer >= self.scatter_limit:
                self.change_mode('chase')
                self.chase_count += 1

        elif self.mode == 'chase':
            if timer >= self.chase_limit and self.chase_count <= 2:
                self.change_mode('scatter')

        elif self.mode == 'frighten':
            if timer >= self.frighten_limit:
                self.change_mode('scatter')
        elif self.mode == 'eaten':
            if self.in_home == 1:
                self.change_mode('scatter')
                self.start_mode = pygame.time.get_ticks()

        ''' ghost movement '''

        if self.movable():
            # make ghost get into the house and change state
            if self.mode == 'eaten':
                if self.grid_pos == self.target:
                    self.direction = Vector2(0,1)

            # move the drawing position by ghost direction and speed
            self.pic_pos.x += self.direction.x * self.speed
            self.pic_pos.y += self.direction.y * self.speed

            # move the grid position if the drawing position is in the correct match with grid position
            if (self.pic_pos[0] + 5) % 20 == 0 and (self.pic_pos[1] + 5) % 20 == 0:
                self.grid_pos += self.direction
                # change in-home state if ghost is in the house entrance
                if self.grid_pos in self.home_en:
                    self.last_dec_point = self.grid_pos
                    if self.in_home == 1:
                        self.in_home = 0
                    else:
                        self.in_home = 1
                # find new grid position of the target
                self.find_target()
                # choose next direction
                if self.grid_pos in self.dec_point:
                    self.last_dec_point = self.grid_pos
                    self.make_decision()

        # make ghost get out of its house
        if self.in_home == 1:
            for i in self.game.ghost_en:
                if self.grid_pos + Vector2(0, -1) == i:
                    self.direction = Vector2(0, -1)

        # FIX if the drawing position does not match with grid position
        if self.mode == 'eaten':
            if self.pic_pos[0] - self.get_pic_pos()[0] != 0 and self.pic_pos[1] - self.get_pic_pos()[1] :
                self.pic_pos = self.get_pic_pos()
            elif self.pic_pos[0] - self.get_pic_pos()[0] > 20:
                self.pic_pos = self.get_pic_pos() + [20,0]
            elif self.get_pic_pos()[0] - self.pic_pos[0] > 20:
                self.pic_pos = self.get_pic_pos() + [-20,0]
            elif self.pic_pos[1] - self.get_pic_pos()[1] > 20:
                self.pic_pos = self.get_pic_pos() + [0,20]
            elif self.get_pic_pos()[1] - self.pic_pos[1] > 20:
                self.pic_pos = self.get_pic_pos() + [0,-20]

    ''' change ghost states'''
    def change_mode(self, mode):
        self.mode = mode
        self.start_mode = pygame.time.get_ticks()
        if mode != 'eaten':
             self.speed = 2
        else:
             self.speed = 4

    ''' reset everything when pac died '''
    def pac_revive(self, position):
        self.grid_pos = position
        self.pic_pos = Vector2((self.grid_pos.x * GRID_SIZE) - 5,
                               (self.grid_pos.y * GRID_SIZE) - 5)
        self.mode = 'scatter'
        self.direction = Vector2(0, -1)
        self.in_home = 1
        self.last_dec_point = None
        self.start_mode = pygame.time.get_ticks()
        self.speed = 2

    @abstractmethod
    def find_target(self):
        pass









