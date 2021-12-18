import pygame
from constant import *

class Pac_Man(object):
    def __init__(self, position, game):
        self.game = game
        self.grid_position = position
        self.pacR = PAC_SIZE / 2
        self.pic_position = Vector2((self.grid_position.x * GRID_SIZE - (self.pacR - GRID_SIZE / 2)),
                                    (self.grid_position.y * GRID_SIZE - (self.pacR - GRID_SIZE / 2)))
        self.pac_state = 'left'
        self.pac_direction = Vector2(-1, 0)
        self.move_count = 0
        self.pic_move_count = Vector2(0,0)
        self.life = 3
        self.status = 'alive'
        self.speed = 2
        self.direction_list = {'left':Vector2(-1,0), 'right':Vector2(1,0), 'up':Vector2(0,-1), 'down':Vector2(0, 1)}

    ''' make Pac change the direction only when that direction is not a wall '''
    def pac_move(self, state):
        if self.turnable(state):
            self.pac_state = state
            self.pac_direction = self.direction_list[state]

    def pac_update(self):
        if self.status != 'dying':
            self.hit_ghost()
            if self.movable():
                self.pic_position[0] += self.pac_direction[0] * self.speed
                self.pic_position[1] += self.pac_direction[1] * self.speed
                self.pic_move_count[0] += self.pac_direction[0] * self.speed
                self.pic_move_count[1] += self.pac_direction[1] * self.speed
            if (self.pic_position[0] + 5) % 20 == 0 and (self.pic_position[1] + 5) % 20 == 0:
                self.grid_position += self.pac_direction
                self.eat_dots()
                self.eat_energizer()
                self.pic_move_count = Vector2(0, 0)

            if self.pic_move_count[0] >= 20 or self.pic_move_count[1] >= 20:
                self.pic_move_count = Vector2(0, 0)

    ''' make pac stop when hit the wall '''
    def movable(self):
        for wall in self.game.walls:
            if self.grid_position + self.pac_direction == wall :
                self.pac_direction = Vector2(0,0)
                return False
        for g in self.game.ghost_en:
            if self.grid_position + self.pac_direction == g:
                self.pac_direction = Vector2(0,0)
                return False
        return True

    ''' check whether there is a wall on that direction or not  '''
    def turnable(self, turn):
        direction = self.direction_list[turn]
        gridX = (self.pic_position[0] + 5) / 20
        gridY = (self.pic_position[1] + 5) / 20
        if (gridX % 1 == 0 and gridY % 1 == 0):
            if Vector2(gridX, gridY) + direction not in self.game.walls and\
                Vector2(gridX, gridY) + direction not in self.game.ghost_en:
                return True
        return False

    ''' remove dot from the dots list '''
    def eat_dots(self):
        if self.grid_position in self.game.dots:
            self.game.eat_sound.play()
            self.game.dots.remove(Vector2(self.grid_position))
            self.game.point += 10

    ''' remove energizer from the energizer list and make ghost become frighten '''
    def eat_energizer(self):
        if self.grid_position in self.game.energ:
            self.game.eat_en.play()
            self.game.energ.remove(self.grid_position)
            for ghost in self.game.ghostList:
                ghost.mode = 'frighten'
                ghost.in_home = 0
                ghost.start_mode = pygame.time.get_ticks()
                if ghost.direction == Vector2(1, 0):
                    ghost.direction = Vector2(-1, 0)
                elif ghost.direction == Vector2(-1, 0):
                    ghost.direction = Vector2(1, 0)
                elif ghost.direction == Vector2(0, 1):
                    ghost.direction = Vector2(0, -1)
                elif ghost.direction == Vector2(0, -1):
                    ghost.direction = Vector2(0, 1)
                ghost.pic_pos = ghost.get_pic_pos()
                ghost.last_dec_point = None
                ghost.speed = 2

    ''' change pac status to dead when pac hit the ghost '''
    def die(self):
        self.life -= 1
        self.game.death_sound.play()
        self.game.start_die = pygame.time.get_ticks()
        self.status = 'dying'
        self.game.pacdeathFrame = 0
        self.speed = 0

    ''' revive PacMan '''
    def revive(self):
        self.grid_position = Vector2(15,23)
        self.pic_position = Vector2((self.grid_position.x * GRID_SIZE - (self.pacR - GRID_SIZE / 2)),
                                    (self.grid_position.y * GRID_SIZE - (self.pacR - GRID_SIZE / 2)))
        self.pac_state = 'left'
        self.pac_direction = Vector2(-1, 0)
        self.move_count = 0
        self.pic_move_count = Vector2(0, 0)
        self.speed = 2

    ''' eat the frightened ghost or die '''
    def hit_ghost(self):
        for ghost in self.game.ghostList:
            if (abs(self.pic_position[0] - ghost.pic_pos[0]) <= 10 and self.pic_position[1] == ghost.pic_pos[1]) or\
                    (abs(self.pic_position[1] - ghost.pic_pos[1]) <= 10 and self.pic_position[0] == ghost.pic_pos[0]):
                if ghost.mode == 'frighten':
                    ghost.pic_pos = ghost.get_pic_pos()
                    ghost.mode = 'eaten'
                    self.game.eat_ghost_sound.play()
                    self.game.point += 750
                    ghost.last_dec_point = Vector2(0, 0)
                    ghost.start_mode = pygame.time.get_ticks()
                    if ghost.grid_pos in ghost.dec_point:
                        ghost.make_decision()
                    ghost.speed = 4
                elif ghost.mode != 'eaten':
                    ghost.pic_pos = ghost.get_pic_pos()
                    self.die()
                    break
