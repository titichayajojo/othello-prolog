try:
    from abc import ABC, abstractmethod
    import pygame
    import math as m
    import random
    from constant import *
except ImportError as i:
    print('File: "ghosts.py" cannot import :', i.name)
else:
    Vector2 = pygame.math.Vector2

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
        turns = [Vector2(0,-1), Vector2(-1,0), Vector2(0,1), Vector2(1,0)]
        dist = []
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
                    break

        if self.mode == 'frighten':
            self.direction = random.choice(turns)
        else:
            for turn in turns:
                dist.append(self.find_distance([self.grid_pos[0]+turn[0],self.grid_pos[1] + turn[1]],
                                               self.target))
            for i in range(len(dist)):
                if dist[i] == min(dist):
                    self.direction = turns[i]
                    return

    def update(self):
        timer = (pygame.time.get_ticks() - self.start_mode) / 1000

        ''' change ghost states '''
        if self.mode == 'scatter':
            if timer >= 7:
                self.change_mode('chase')

        elif self.mode == 'chase':
            if timer >= 20:
                self.change_mode('scatter')

        elif self.mode == 'frighten':
            if timer >= 10:
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


class Blinky(Ghost):
    def __init__(self, position, game, pac):
        super().__init__(position, game, pac)
        self.direction = Vector2(1,0)
        self.in_home = 0

    ''' find grid position of the target '''
    def find_target(self):
        if self.mode == 'eaten':
            self.target = Vector2(13,11)
        # scatter mode : top right corner of the maze
        elif self.mode == 'scatter':
            self.target = Vector2(25,0)
        # chase mode : position of Pac
        elif self.mode == 'chase':
            self.target = self.pac.grid_position

    def pac_revive(self, position):
        super().pac_revive(position)
        self.in_home = 0
        self.direction = Vector2(1,0)

    def __str__(self):
        return "Blinky"


class Pinky(Ghost):
    def find_target(self):
        if self.mode == 'eaten':
            self.target = Vector2(13,11)
        # scatter mode : top left corner of the maze
        elif self.mode == 'scatter':
            self.target = Vector2(1,0)
        # chase mode : four block in front of Pac
        elif self.mode == 'chase':
            if self.pac.pac_direction == [0,-1]:
                self.target = self.pac.grid_position + [-4,-4]
            else:
                self.target = Vector2(self.pac.grid_position.x + self.pac.pac_direction.x * 4,
                                      self.pac.grid_position.y + self.pac.pac_direction.y * 4)

    def __str__(self):
        return "Pinky"


class Inky(Ghost):
    def __init__(self, position, game, pac, blinky):
        super().__init__(position,game,pac)
        self.blink = blinky

    def find_target(self):
        if self.mode == 'eaten':
            self.target = Vector2(13,11)
        # scatter mode : bottom left corner of the maze
        elif self.mode == 'scatter':
            self.target = Vector2(27,30)
        # chase mode : two block in front of the Pac is temporary position
        #              opposite direction of the temporary position and Blinky position is Inky's target
        elif self.mode == 'chase':
            if self.pac.pac_direction == Vector2(0, -1):
                temp_target = self.pac.grid_position + Vector2(2, 2)
            else:
                temp_target = self.pac.grid_position + [self.pac.pac_direction[0] * 2,
                                                        self.pac.pac_direction[1] * 2]
            difference = Vector2(abs(self.blink.grid_pos[0] - temp_target[0]), \
                                 abs(self.blink.grid_pos[1] - temp_target[1]))
            self.target = temp_target - difference

    def __str__(self):
        return "Inky"


class Clyde(Ghost):
    def find_target(self):
        if self.mode == 'eaten':
            self.target = Vector2(13,11)
        # scatter mode : bottom left corner of the maze
        elif self.mode == 'scatter':
            self.target = Vector2(0,30)
        # chase mode : if Pac is eight blocks away from Clyde,
        #               Clyde will target the Pac position
        elif self.mode == 'chase':
            if self.find_distance(self.grid_pos, self.pac.grid_position) <= 8:
                self.target = self.pac.grid_position
            else:
                self.target = Vector2(0, 30)

    def __str__(self):
        return "Clyde"


