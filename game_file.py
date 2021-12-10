try:
    import pygame
    from constant import *
    from ghosts_class import *
    from pac_class import *
except ImportError as ie:
    print('File: "game_file.py" cannot import :',ie.name)
else:
    Vector2 = pygame.math.Vector2
    pygame.init()

class Game(object):
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.running = True
        self.walls = []
        self.dots = []
        self.energ = []
        self.ghost_en = []
        self.ghost_dec = []
        self.pac_start = None
        self.blinky_start = None
        self.inky_start = None
        self.pinky_start = None
        self.clyde_start = None
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        try:
            self.load_elements()
        except CannotOpenFile as c:
            print('Cannot open file:',CannotOpenFile.filename)
            self.running = 0
        except pygame.error:
            print(pygame.get_error())
            self.running = 0
        else:
            self.pac = Pac_Man(self.pac_start,self)
            self.blinky = Blinky(self.blinky_start, self, self.pac)
            self.pinky = Pinky(self.pinky_start, self, self.pac)
            self.inky = Inky(self.inky_start, self, self.pac, self.blinky)
            self.clyde = Clyde(self.clyde_start, self, self.pac)
            pygame.display.set_icon(self.icon)
            self.ghost_moveCount = 0
            self.pac_turn = 'left'
            self.win = False
            self.win_streak = 0
            self.start_die = 0
            self.pacdeathFrame = 0
            self.point = 0
            self.ghostList = [self.blinky, self.pinky, self.inky, self.clyde]
            self.scene = 'menu'

    ''' main game loop '''
    def run(self):
        self.played = 1
        while self.running:
            if self.scene == 'menu':
                key = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                self.draw_menu()
                if START_BUT_POS[0] + START_BUT_WIDTH > mouse[0] > START_BUT_POS[0] and \
                        START_BUT_POS[1] + START_BUT_HEIGHT > mouse[1] > START_BUT_POS[1]:
                    if click[0]:
                        self.start_ticks = pygame.time.get_ticks()
                        self.scene = 'playing'
                        self.beginning_sound.play()
                        self.window.fill(BLACK)
                        self.window.blit(self.bg, (0, 0))
                        self.draw_dots()
                        self.draw_score_life()
                        for ghost in self.ghostList:
                            ghost.start_mode = pygame.time.get_ticks() + 4150

                if EXIT_BUT_POS[0] + EXIT_BUT_WIDTH > mouse[0] > EXIT_BUT_POS[0] and \
                        EXIT_BUT_POS[1] + EXIT_BUT_HEIGHT > mouse[1] > EXIT_BUT_POS[1]:
                    if click[0]:
                        break
            elif self.scene == 'playing':
                seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
                dying = (pygame.time.get_ticks() - self.start_die) / 1000
                if seconds <= 4.15 and self.win != -1:
                    if self.played == 0:
                        self.played = 1
                        self.beginning_sound.play()
                        self.prepare_game()
                else:
                    if dying <= 2.1:
                        self.redraw_game()
                        self.draw_die()
                    elif dying > 2.1 and dying <= 2.2:
                        self.start_die = 0
                        self.revive()
                        self.pac.revive()
                    else:
                        self.pac.status = 'alive'
                        self.user_interact()
                        if self.pac.turnable(self.pac_turn):
                            self.pac.pac_move(self.pac_turn)
                        if self.win == 0:
                            self.pac.pac_update()
                            self.blinky.update()
                            self.inky.update()
                            self.pinky.update()
                            self.clyde.update()
                            if self.dots == []:
                                self.win = 1
                            self.redraw_game()
                            if self.pac.life == 0:
                                self.win = -1
                        
                        elif self.win == -1 or self.win_streak == 5:
                            self.scene = 'end'
                            if self.win_streak == 5:
                                self.win = 1
                            
                        elif self.win == 1:
                            self.win_streak += 1
                            self.scene = 'continue'
                        self.draw_score_life()

            elif self.scene == 'continue':
                seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
                dying = (pygame.time.get_ticks() - self.start_die) / 1000
                self.next_level()
                self.scene = 'playing'
                self.beginning_sound.play()

            elif self.scene == 'end':
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
                    dying = (pygame.time.get_ticks() - self.start_die) / 1000
                    self.restart_game()
                    self.scene = 'playing'
                    self.beginning_sound.play()
                elif key[pygame.K_ESCAPE]:
                    self.restart_game()
                    self.scene = 'menu'
                self.end_draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()

    ''' draw playing scene '''
    def redraw_game(self):
        self.window.fill(BLACK)
        self.window.blit(self.bg, (0, 0))
        self.draw_dots()
        self.draw_ghost()
        self.draw_pac()

    ''' draw preparing scene '''
    def prepare_game(self):
        self.window.fill(BLACK)
        self.window.blit(self.bg, (0, 0))
        self.draw_dots()
        self.draw_score_life()

    ''' draw Pac Man '''
    def draw_pac(self):
        if self.pac.status != 'dying':
            if self.pac.move_count + 1 >= 12:
                self.pac.move_count = 0

            if self.pac.pac_state == 'left':
                self.window.blit(self.pacLeft[self.pac.move_count // 4], self.pac.pic_position)
            elif self.pac.pac_state == 'right':
                self.window.blit(self.pacRight[self.pac.move_count // 4], self.pac.pic_position)
            elif self.pac.pac_state == 'up':
                self.window.blit(self.pacUp[self.pac.move_count // 4], self.pac.pic_position)
            elif self.pac.pac_state == 'down':
                self.window.blit(self.pacDown[self.pac.move_count // 4], self.pac.pic_position)

            self.pac.move_count += 1

    ''' draw every ghost'''
    def draw_ghost(self):
        if self.ghost_moveCount + 1 >= 8:
            self.ghost_moveCount = 0

        if self.blinky.mode == 'frighten':
            self.window.blit(self.frightenSprite[self.ghost_moveCount // 4], self.blinky.pic_pos)
        elif self.blinky.mode == 'eaten':
            self.window.blit(self.eatenSprite, self.blinky.pic_pos)
        else:
            if self.blinky.direction == Vector2(-1, 0):
                self.window.blit(self.blinkyLeft[self.ghost_moveCount // 4], self.blinky.pic_pos)
            elif self.blinky.direction == Vector2(1, 0):
                self.window.blit(self.blinkyRight[self.ghost_moveCount // 4], self.blinky.pic_pos)
            elif self.blinky.direction == Vector2(0, -1):
                self.window.blit(self.blinkyUp[self.ghost_moveCount // 4], self.blinky.pic_pos)
            elif self.blinky.direction == Vector2(0, 1):
                self.window.blit(self.blinkyDown[self.ghost_moveCount // 4], self.blinky.pic_pos)

        if self.pinky.mode == 'frighten':
            self.window.blit(self.frightenSprite[self.ghost_moveCount // 4], self.pinky.pic_pos)
        elif self.pinky.mode == 'eaten':
            self.window.blit(self.eatenSprite, self.pinky.pic_pos)
        else:
            if self.pinky.direction == Vector2(-1, 0):
                self.window.blit(self.pinkyLeft[self.ghost_moveCount // 4], self.pinky.pic_pos)
            elif self.pinky.direction == Vector2(1, 0):
                self.window.blit(self.pinkyRight[self.ghost_moveCount // 4], self.pinky.pic_pos)
            elif self.pinky.direction == Vector2(0, -1):
                self.window.blit(self.pinkyUp[self.ghost_moveCount // 4], self.pinky.pic_pos)
            elif self.pinky.direction == Vector2(0, 1):
                self.window.blit(self.pinkyDown[self.ghost_moveCount // 4], self.pinky.pic_pos)

        if self.inky.mode == 'frighten':
            self.window.blit(self.frightenSprite[self.ghost_moveCount // 4], self.inky.pic_pos)
        elif self.inky.mode == 'eaten':
            self.window.blit(self.eatenSprite, self.inky.pic_pos)
        else:
            if self.inky.direction == Vector2(-1, 0):
                self.window.blit(self.inkyLeft[self.ghost_moveCount // 4], self.inky.pic_pos)
            elif self.inky.direction == Vector2(1, 0):
                self.window.blit(self.inkyRight[self.ghost_moveCount // 4], self.inky.pic_pos)
            elif self.inky.direction == Vector2(0, -1):
                self.window.blit(self.inkyUp[self.ghost_moveCount // 4], self.inky.pic_pos)
            elif self.inky.direction == Vector2(0, 1):
                self.window.blit(self.inkyDown[self.ghost_moveCount // 4], self.inky.pic_pos)

        if self.clyde.mode == 'frighten':
            self.window.blit(self.frightenSprite[self.ghost_moveCount // 4], self.clyde.pic_pos)
        elif self.clyde.mode == 'eaten':
            self.window.blit(self.eatenSprite, self.clyde.pic_pos)
        else:
            if self.clyde.direction == Vector2(-1, 0):
                self.window.blit(self.clydeLeft[self.ghost_moveCount // 4], self.clyde.pic_pos)
            elif self.clyde.direction == Vector2(1, 0):
                self.window.blit(self.clydeRight[self.ghost_moveCount // 4], self.clyde.pic_pos)
            elif self.clyde.direction == Vector2(0, -1):
                self.window.blit(self.clydeUp[self.ghost_moveCount // 4], self.clyde.pic_pos)
            elif self.clyde.direction == Vector2(0, 1):
                self.window.blit(self.clydeDown[self.ghost_moveCount // 4], self.clyde.pic_pos)
        self.ghost_moveCount += 1

    ''' draw every elements in different grid color '''
    def draw_grid(self):
        for x in range (MAZE_WIDTH // GRID_SIZE):
            pygame.draw.line(self.bg, GREY, (GRID_SIZE * x, 0), (GRID_SIZE * x, MAZE_HEIGHT))
        for y in range (MAZE_HEIGHT // GRID_SIZE):
            pygame.draw.line(self.bg, GREY, (0, y * GRID_SIZE), (MAZE_WIDTH, y * GRID_SIZE))
        for wall in self.walls:
            pygame.draw.rect(self.bg, LIGHT_BLUE, (wall.x * GRID_SIZE,
                                                    wall.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for dot in self.dots:
            pygame.draw.rect(self.bg, WHITE, (dot.x * GRID_SIZE,
                                                    dot.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for en in self.energ:
            pygame.draw.rect(self.bg, GREEN, (en.x * GRID_SIZE,
                                                    en.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for g in self.ghost_en:
            pygame.draw.rect(self.bg, PURPLE, (g.x * GRID_SIZE,
                                              g.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for d in self.ghost_dec:
            pygame.draw.rect(self.bg, BLUE, (d.x * GRID_SIZE,d.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(self.window, TURQUOISE, (self.inky.target[0] * GRID_SIZE,
                                              self.inky.target[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.window, RED, (self.blinky.target[0] * GRID_SIZE,
                                              self.blinky.target[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.window, PINK, (self.pinky.target[0] * GRID_SIZE,
                                              self.pinky.target[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.window, ORANGE, (self.clyde.target[0] * GRID_SIZE,
                                              self.clyde.target[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.window, TURQUOISE, (self.inky.grid_pos[0] * GRID_SIZE,
                                                  self.inky.grid_pos[1] * GRID_SIZE, GRID_SIZE,GRID_SIZE))
        pygame.draw.rect(self.window, RED, (self.blinky.grid_pos[0] * GRID_SIZE,
                                            self.blinky.grid_pos[1] * GRID_SIZE, GRID_SIZE,GRID_SIZE))
        pygame.draw.rect(self.window, PINK, (self.pinky.grid_pos[0] * GRID_SIZE,
                                             self.pinky.grid_pos[1] * GRID_SIZE, GRID_SIZE,GRID_SIZE))
        pygame.draw.rect(self.window, ORANGE, (self.clyde.grid_pos[0] * GRID_SIZE,
                                               self.clyde.grid_pos[1] * GRID_SIZE, GRID_SIZE,GRID_SIZE))
        pygame.draw.rect(self.window, YELLOW, (self.pac.grid_position[0] * GRID_SIZE,
                                               self.pac.grid_position[1] * GRID_SIZE, GRID_SIZE,GRID_SIZE))

    ''' get key press from keyboard '''
    def user_interact(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.pac_turn = 'left'
        elif key[pygame.K_RIGHT]:
            self.pac_turn = 'right'
        elif key[pygame.K_UP]:
            self.pac_turn = 'up'
        elif key[pygame.K_DOWN]:
            self.pac_turn = 'down'
        elif key[pygame.K_k]:
            self.win = 1
        elif key[pygame.K_l]:
            self.win = -1

    ''' load every resources '''
    def load_elements(self):
        filedirect = 'resources/maze_data.txt'
        try:
            inFile = open(filedirect,'r')
            self.icon = pygame.image.load('resources/app_logo.png')
            self.pacLeft = [pygame.image.load('resources/sprites/pac/pacman 0.png'), pygame.image.load('resources/sprites/pac/pacleft1.png'),
                            pygame.image.load('resources/sprites/pac/pacleft2.png')]

            self.pacRight = [pygame.image.load('resources/sprites/pac/pacman 0.png'), pygame.image.load('resources/sprites/pac/pacright1.png'),
                             pygame.image.load('resources/sprites/pac/pacright2.png')]

            self.pacUp = [pygame.image.load('resources/sprites/pac/pacman 0.png'), pygame.image.load('resources/sprites/pac/pacup1.png'),
                          pygame.image.load('resources/sprites/pac/pacup2.png')]

            self.pacDown = [pygame.image.load('resources/sprites/pac/pacman 0.png'), pygame.image.load('resources/sprites/pac/pacdown1.png'),
                            pygame.image.load('resources/sprites/pac/pacdown2.png')]

            self.blinkyLeft = [pygame.image.load('resources/sprites/blinky/blinkyleft.png'), pygame.image.load('resources/sprites/blinky/blinkyleft2.png')]
            self.blinkyRight = [pygame.image.load('resources/sprites/blinky/blinkyright.png'),
                                pygame.image.load('resources/sprites/blinky/blinkyright2.png')]
            self.blinkyUp = [pygame.image.load('resources/sprites/blinky/blinkyup.png'), pygame.image.load('resources/sprites/blinky/blinkyup2.png')]
            self.blinkyDown = [pygame.image.load('resources/sprites/blinky/blinkydown.png'), pygame.image.load('resources/sprites/blinky/blinkydown2.png')]

            self.pinkyLeft = [pygame.image.load('resources/sprites/pinky/pinkleft.png'), pygame.image.load('resources/sprites/pinky/pinkleft2.png')]
            self.pinkyRight = [pygame.image.load('resources/sprites/pinky/pinkyright.png'), pygame.image.load('resources/sprites/pinky/pinkyright2.png')]
            self.pinkyUp = [pygame.image.load('resources/sprites/pinky/pinkyup.png'), pygame.image.load('resources/sprites/pinky/pinkyup2.png')]
            self.pinkyDown = [pygame.image.load('resources/sprites/pinky/pinkydown.png'), pygame.image.load('resources/sprites/pinky/pinkydown2.png')]

            self.inkyLeft = [pygame.image.load('resources/sprites/inky/inkyleft.png'), pygame.image.load('resources/sprites/inky/inkyleft2.png')]
            self.inkyRight = [pygame.image.load('resources/sprites/inky/inkyright.png'), pygame.image.load('resources/sprites/inky/inkyright2.png')]
            self.inkyUp = [pygame.image.load('resources/sprites/inky/inkyup.png'), pygame.image.load('resources/sprites/inky/inkyup2.png')]
            self.inkyDown = [pygame.image.load('resources/sprites/inky/inkydown.png'), pygame.image.load('resources/sprites/inky/inkydown2.png')]

            self.clydeLeft = [pygame.image.load('resources/sprites/clyde/clydeleft.png'), pygame.image.load('resources/sprites/clyde/clydeleft2.png')]
            self.clydeRight = [pygame.image.load('resources/sprites/clyde/clyderight.png'), pygame.image.load('resources/sprites/clyde/clyderight2.png')]
            self.clydeUp = [pygame.image.load('resources/sprites/clyde/clydeup.png'), pygame.image.load('resources/sprites/clyde/clydeup2.png')]
            self.clydeDown = [pygame.image.load('resources/sprites/clyde/clydedown.png'), pygame.image.load('resources/sprites/clyde/clydedown2.png')]
            
            self.pacdeath = [pygame.image.load('resources/sprites/pac/death1.png'), pygame.image.load('resources/sprites/pac/death2.png'),
                             pygame.image.load('resources/sprites/pac/death3.png'), pygame.image.load('resources/sprites/pac/death4.png'),
                             pygame.image.load('resources/sprites/pac/death5.png'), pygame.image.load('resources/sprites/pac/death6.png'),
                             pygame.image.load('resources/sprites/pac/death7.png'), pygame.image.load('resources/sprites/pac/death8.png'),
                             pygame.image.load('resources/sprites/pac/death9.png'), pygame.image.load('resources/sprites/pac/death10.png'),
                             pygame.image.load('resources/sprites/pac/death11.png'), pygame.image.load('resources/sprites/pac/death11.png'),
                             pygame.image.load('resources/sprites/pac/death11.png')]

            self.frightenSprite = [pygame.image.load('resources/sprites/frighten/frighten.png'),
                                   pygame.image.load('resources/sprites/frighten/frighten2.png')]
            self.eatenSprite = pygame.image.load('resources/sprites/eaten/eaten.png')
            self.bg = pygame.image.load('resources/maze_background.png')
            self.winscene = pygame.image.load('resources/gamescenes/winscene.png')
            self.losescene = pygame.image.load('resources/gamescenes/losescene.png')
            self.menuscene = pygame.image.load('resources/gamescenes/menuscene.png')
            self.eat_sound = pygame.mixer.Sound("resources/sounds/sound_chomp.wav")
            self.beginning_sound = pygame.mixer.Sound("resources/sounds/sound_beginning.wav")
            self.eat_en = pygame.mixer.Sound("resources/sounds/sound_eatfruit.wav")
            self.death_sound = pygame.mixer.Sound("resources/sounds/sound_death.wav")
            self.eat_ghost_sound = pygame.mixer.Sound("resources/sounds/sound_eatghost.wav")

        except FileNotFoundError:
            raise  CannotOpenFile(FileNotFoundError.filename)
        except pygame.error:
            raise pygame.error
        else:
            data = inFile.readlines()
            # load grid information from maze.txt
            for y, line in enumerate(data):
                for x, character in enumerate(line):
                    if character == '1':
                        self.walls.append(Vector2(x, y))
                    elif character == 'D':
                        self.dots.append(Vector2(x, y))
                    elif character == 'E':
                        self.energ.append(Vector2(x, y))
                    elif character == 'B':
                        self.blinky_start = Vector2(x, y)
                    elif character == 'I':
                        self.inky_start = Vector2(x, y)
                    elif character == 'P':
                        self.pinky_start = Vector2(x, y)
                    elif character == 'C':
                        self.clyde_start = Vector2(x, y)
                    elif character == 'M':
                        self.pac_start = Vector2(x, y)
                    elif character == 'G':
                        self.ghost_en.append(Vector2(x,y))
                    elif character == 'K':
                        self.ghost_dec.append((Vector2(x,y)))
                    elif character == 'X':
                        self.ghost_dec.append(Vector2(x,y))
                        self.dots.append((Vector2(x,y)))
        inFile.close()

    ''' function use to draw text on the screen '''
    def create_text(self, string, space, pos, fontSize, color, font_name, centered = False):
        font = pygame.font.Font(font_name, fontSize)
        text = font.render(string, False, color)
        if centered:
            pos =  [pos[0] - text.get_size()[0] // 2, pos[1] - text.get_size()[1] // 2]
        space.blit(text, pos)

    def draw_dots(self):
        for dot in self.dots:
            pygame.draw.circle(self.window, WHITE, (int(dot.x * GRID_SIZE) + GRID_SIZE // 2,
                                int(dot.y * GRID_SIZE) + GRID_SIZE // 2), 3 )
        for e in self.energ:
            pygame.draw.circle(self.window, WHITE, (int(e.x * GRID_SIZE) + GRID_SIZE // 2,
                                                int(e.y * GRID_SIZE) + GRID_SIZE // 2), 7)

    ''' draw ending scene '''
    def end_draw(self):
        if self.win == 1:
            self.window.blit(self.winscene, (0,0))
            self.create_text('{}'.format(self.point),
                             self.window, [420, 135], 60, BRIGHT_GREEN, ARC_FONT, True)
        elif self.win == -1:
            self.window.blit(self.losescene, (0,0))
            self.create_text('{}'.format(self.point),
                             self.window, [420, 135], 60, RED, ARC_FONT, True)
        self.create_text('SCORE:'.format(self.point),
                         self.window, [420, 75], 30, WHITE, ARC_FONT, True)

        pygame.display.update()
    
    def revive(self):
        self.blinky.pac_revive(Vector2(14, 11))
        self.pinky.pac_revive(Vector2(14,14))
        self.inky.pac_revive(Vector2(12, 14))
        self.clyde.pac_revive(Vector2(16,14))
        self.start_ticks = pygame.time.get_ticks()
        self.played = 0
        self.pac_turn = 'left'

    ''' Pac dead '''
    def draw_die(self):
        if self.pacdeathFrame <= 51:
            self.window.blit(self.pacdeath[self.pacdeathFrame // 4], self.pac.pic_position)
        self.pacdeathFrame += 1

    ''' draw menu scene '''
    def draw_menu(self):
        self.window.blit(self.menuscene, (0,0))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        start_pos = [START_BUT_POS[0] + START_BUT_WIDTH / 2, START_BUT_POS[1] + START_BUT_HEIGHT / 2]
        exit_pos = [EXIT_BUT_POS[0] + EXIT_BUT_WIDTH / 2 + 2, EXIT_BUT_POS[1] + EXIT_BUT_HEIGHT / 2 + 2]
        self.create_text('by JoJo Rit Pun', self.window, [360, 635], 8, WHITE, ARC_FONT, True)
        if START_BUT_POS[0] + START_BUT_WIDTH > mouse[0] > START_BUT_POS[0] and\
                START_BUT_POS[1] + START_BUT_HEIGHT > mouse[1] > START_BUT_POS[1] :
            pygame.draw.rect(self.window, WHITE,
                             (START_BUT_POS[0] - 2, START_BUT_POS[1] - 2, START_BUT_WIDTH + 4, START_BUT_HEIGHT + 4))
            pygame.draw.rect(self.window, BRIGHT_GREEN, (START_BUT_POS[0], START_BUT_POS[1], START_BUT_WIDTH, START_BUT_HEIGHT))
            self.create_text('start', self.window, start_pos, 32, BLACK, PAC_FONT, True)
        else:
            pygame.draw.rect(self.window, FOREST_GREEN,
                             (START_BUT_POS[0] - 2, START_BUT_POS[1] - 2, START_BUT_WIDTH + 4, START_BUT_HEIGHT + 4))
            pygame.draw.rect(self.window, DARK_GREY, (START_BUT_POS[0], START_BUT_POS[1], START_BUT_WIDTH, START_BUT_HEIGHT))
            self.create_text('start', self.window, start_pos, 32, SELECTIVE_YELLOW, PAC_FONT, True)

        if EXIT_BUT_POS[0] + EXIT_BUT_WIDTH > mouse[0] > EXIT_BUT_POS[0] and \
                EXIT_BUT_POS[1] + EXIT_BUT_HEIGHT > mouse[1] > EXIT_BUT_POS[1]:
            pygame.draw.rect(self.window, WHITE,
                             (EXIT_BUT_POS[0], EXIT_BUT_POS[1], EXIT_BUT_WIDTH + 4, EXIT_BUT_HEIGHT + 4))
            pygame.draw.rect(self.window, RED,
                             (EXIT_BUT_POS[0] + 2, EXIT_BUT_POS[1] + 2, EXIT_BUT_WIDTH, EXIT_BUT_HEIGHT))
            self.create_text('exit', self.window, exit_pos, 18, BLACK, PAC_FONT, True)

        else:
            pygame.draw.rect(self.window, RED,
                             (EXIT_BUT_POS[0], EXIT_BUT_POS[1], EXIT_BUT_WIDTH + 4, EXIT_BUT_HEIGHT + 4))
            pygame.draw.rect(self.window, DARK_GREY,
                             (EXIT_BUT_POS[0] + 2, EXIT_BUT_POS[1] + 2, EXIT_BUT_WIDTH, EXIT_BUT_HEIGHT))
            self.create_text('exit', self.window, exit_pos, 18, WHITE, PAC_FONT, True)

        pygame.display.update()

    ''' draw score and life under the maze '''
    def draw_score_life(self):
        self.create_text('SCORE: {}'.format(self.point),
                         self.window, [50, 630], 22, WHITE, ARC_FONT)
        self.create_text('LIFE: {}'.format(self.pac.life),
                         self.window, [350, 630], 22, FOREST_GREEN, ARC_FONT)

    ''' restart the game and reset every elements '''
    def restart_game(self):
        self.walls = []
        self.dots = []
        self.energ = []
        self.ghost_en = []
        self.ghost_dec = []
        self.point = 0
        self.win = 0
        self.win_streak = 0
        self.start_ticks = pygame.time.get_ticks()
        self.load_elements()
        self.pac = Pac_Man(self.pac_start,self)
        self.blinky = Blinky(self.blinky_start, self, self.pac)
        self.pinky = Pinky(self.pinky_start, self, self.pac)
        self.inky = Inky(self.inky_start, self, self.pac, self.blinky)
        self.clyde = Clyde(self.clyde_start, self, self.pac)
        self.start_die = 0
        self.pac.pac_state = 'left'
        self.pac.pac_direction = Vector2(-1, 0)
        self.pac.life = 3
        self.ghostList = [self.blinky, self.pinky, self.clyde, self.inky]
        for ghost in self.ghostList:
            ghost.mode = 'scatter'
            ghost.start_mode = pygame.time.get_ticks() + 4150

    def next_level(self):
        self.walls = []
        self.dots = []
        self.energ = []
        self.ghost_en = []
        self.ghost_dec = []
        self.win = 0
        self.start_ticks = pygame.time.get_ticks()
        self.load_elements()
        self.pac = Pac_Man(self.pac_start,self)
        self.blinky = Blinky(self.blinky_start, self, self.pac)
        self.pinky = Pinky(self.pinky_start, self, self.pac)
        self.inky = Inky(self.inky_start, self, self.pac, self.blinky)
        self.clyde = Clyde(self.clyde_start, self, self.pac)
        self.pac.pac_state = 'left'
        self.pac.pac_direction = Vector2(-1, 0)
        self.ghostList = [self.blinky, self.pinky, self.clyde, self.inky]
        for ghost in self.ghostList:
            ghost.mode = 'scatter'
            ghost.start_mode = pygame.time.get_ticks() + 4150

