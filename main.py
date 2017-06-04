import pygame
import math

####constants####
WIDTH = 800 # 800 adjusted for map 25x25: 373
HEIGHT = 600 # 600 adjusted for map 25x25  405
#colors#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
BROWN = (102, 51, 0)
ROBBO_GREEN = (0, 150, 0)
########
#chars#
char_PLAYER = '@'
char_WALL = '#'
char_SPACE = '.'
char_EMPTY = ' '
char_STAIR_DOWN = '>' # when going to the next level, offload the status of current level to a new file, and then read that updated file
char_STAIR_UP = '<'
char_SCREW = '*'
char_BARREL = 'O'
char_SIZE = 15
########
MAX_NUMBER_LEVELS = 2
#LEVEL_NUM = 2
################

#classes#
# TODO MAKE A WORLD CLASS, WHICH WILL BE GOING TO HAVE ALL OF DATA


class PlayerClass: # will be the player and the barrel

    def __init__(self, x, y, hp=None, screws=None):
        self.x = x
        self.y = y
        self.hp = hp
        self.screws = screws

    def move(self, dx, dy):
        if not (self.x + dx, self.y + dy) in WALL_LIST:
            self.x += dx
            self.y += dy

    def take(self, gathering_list, bin):
        try:
            for g in gathering_list:
                if distance(Player.x, Player.y, g[0], g[1]) < 2:
                    gathering_list.remove((g[0], g[1]))
                    bin.append((g[0], g[1]))
                    self.screws += 1 # it shouldn't be the exact thing we are gathering, but it's not needed to fix
        except ValueError:
            pass

    def draw(self, icon):
        WINDOW.blit(icon, (self.x, self.y))

    def push(self, pushable_list, bin):
        for p1 in pushable_list:
            if distance(p1[0].x, p1[0].y, self.x, self.y) < 2:
                print p1[0].x, p1[0].y
                if not (p1[0].x + char_SIZE) in BARREL_INSTANCES:
                    p1[0].x += char_SIZE
                #bin.append((p1[0].x, p1[0].y))


class BarrelClass:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        if not (self.x + dx, self.y + dy) in WALL_LIST or BARREL_INSTANCES:
            self.x += dx
            self.y += dy

    def draw(self, icon):
        pass

#GAME#

def game_loop():
    global game_QUIT
    global descend
    game_QUIT = False

    while not game_QUIT:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                game_QUIT = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit(0)
                elif event.key == pygame.K_UP:
                    Player.move(0, -15)
                elif event.key == pygame.K_DOWN:
                    Player.move(0, 15)
                elif event.key == pygame.K_LEFT:
                    Player.move(-15, 0)
                elif event.key == pygame.K_RIGHT:
                    Player.move(15, 0)
                elif event.key == pygame.K_d:
                    #descend = True # change map descent not present in this version
                    # TODO MAKE MULTIPLE LEVELS
                    pass

        game_logic()

def initialize_game():

    global WINDOW
    global PLAYER
    global WALL
    global SPACE
    global EMPTY_SPACE
    global STAIR_DOWN
    global STAIR_UP
    global SCREW
    global BARREL
    global TEXT

    pygame.init()
    pygame.font.init()

    FONT = pygame.font.SysFont('px437ati8x8', char_SIZE)
    PLAYER = FONT.render(char_PLAYER, 0, ROBBO_GREEN)
    WALL = FONT.render(char_WALL, 0, WHITE)
    SPACE = FONT.render(char_SPACE, 0, WHITE)
    EMPTY_SPACE = FONT.render(char_EMPTY, 0, WHITE)
    STAIR_DOWN = FONT.render(char_STAIR_DOWN, 0, WHITE)
    STAIR_UP = FONT.render(char_STAIR_UP, 0, WHITE)
    SCREW = FONT.render(char_SCREW, 0, GREY)
    BARREL = FONT.render(char_BARREL, 0, BROWN)
    TEXT = FONT.render('HP:  Screws:  Level: ', 0, WHITE)

    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


#def getall_maps():
#    global maps_list
#    maps_list = []
#    for f in range (1, MAX_NUMBER_LEVELS):
#        with open('level_%s.txt' % MAX_NUMBER_LEVELS, 'r') as maps:  # < - appending line to a new list, containing each of the levels
#            maps_list.append([maps])
#    print maps_list

def check_if_descended():
    if distance(Player.x, Player.y, st_u_x, st_u_y) < 2:
        return True

def getcurrent_map():
    global current_level
    current_level = []
    current_level_number = 1
    with open('level_%s.txt' % current_level_number, 'r') as l_map:
        for line in l_map:
            current_level.append(line)
    return current_level


def get_obj(char_obj): # getting x,y individually for objects
    lvl = getcurrent_map()
    for y in range(len(lvl)):
        for x in range(len(lvl[y])):
            char = lvl[y][x]

            char_x = 0 + (x * char_SIZE)
            char_y = 0 + (y * char_SIZE)

            if char == char_obj:
                obj_x, obj_y = (char_x, char_y)
                return obj_x, obj_y

player_x, player_y = get_obj(char_PLAYER)
Player = PlayerClass(player_x, player_y, 100, 0)

#DRAWING#

def get_objs():
    # The only aim for this function is to set position to every defined character on screen

    # THIS IS GETTING AND LOOPING FOREVER THE LISTS, THIS HAS TO BE DONE OUTSIDE THE LOOP!!! < - Done
    # commented blocks are my mistakes

    global space_x, space_y
    global starting_x, starting_y
    global wall_x, wall_y
    global st_d_x, st_d_y
    global st_u_x, st_u_y
    global scr_x, scr_y
    global b_x, b_y
    global WALL_LIST
    global SCREW_LIST
    global SPACE_LIST
    global EMPTY_LIST
    global BARREL_LIST
    global Barrel
    global BARREL_INSTANCES

    EMPTY_LIST = []
    WALL_LIST = []
    SCREW_LIST = []
    SPACE_LIST = []
    BARREL_LIST = []
    BARREL_INSTANCES = []

    level = current_level
    for y in range(len(level)):
        for x in range(len(level[y])):
            char = level[y][x]

            char_x = 0 + (x * char_SIZE)
            char_y = 0 + (y * char_SIZE)
            # TODO use get_objects and use for loop to draw objects

            if char == char_WALL:
                wall_x, wall_y = (char_x, char_y)
                WALL_LIST.append((wall_x, wall_y))
                #WINDOW.blit(WALL, (wall_x, wall_y))
                #print wall_x, wall_y

            elif char == char_PLAYER:
                (starting_x, starting_y) = (char_x, char_y) # starting position

                #if distance(Player.x, Player.y, starting_x, starting_y) > 2:
                #    WINDOW.blit(SPACE, (starting_x, starting_y)) # if it's not on it's starting pos, draw '.'

            elif char == char_SPACE:
                (space_x, space_y) = (char_x, char_y)
                SPACE_LIST.append((space_x, space_y))
                #if distance(Player.x, Player.y, space_x, space_y) > 2:
                #    WINDOW.blit(SPACE, (space_x, space_y))
                #print space_x, space_x

            elif char == char_STAIR_DOWN:
                (st_d_x, st_d_y) = (char_x, char_y)
                #if distance(Player.x, Player.y, st_d_x, st_d_y) > 2:
                #        WINDOW.blit(STAIR_DOWN, (st_d_x, st_d_y))
                #else:
                #    (space_x, space_y) = (char_x, char_y)
                #    if distance(Player.x, Player.y, space_x, space_y) > 2:
                #        WINDOW.blit(SPACE, (space_x, space_y))

            elif char == char_STAIR_UP:
                (st_u_x, st_u_y) = (char_x, char_y)
                #if distance(Player.x, Player.y, st_u_x, st_u_y) > 2:
                #    WINDOW.blit(STAIR_UP, (st_u_x, st_u_y))
                # stairs up will be generated next to the place, where the staris down were, if the place will not be occupied.

            elif char == char_SCREW:
                (scr_x, scr_y) = (char_x, char_y) # starting position
                SCREW_LIST.append((scr_x, scr_y))

            elif char == char_EMPTY:
                (e_x, e_y) = (char_x, char_y)
                EMPTY_LIST.append((e_x, e_y))

            elif char == char_BARREL:
                (b_x, b_y) = (char_x, char_y) # starting position of the barrels
                for b in char:
                    Barrel = BarrelClass(b_x, b_y)
                    BARREL_INSTANCES.append([Barrel])
                #BARREL_LIST.append([Barrel.x, Barrel.y])



                #if (scr_x, scr_y) in SCREWS_LIST and distance(Player.x, Player.y, scr_x, scr_y) > 2:
                #    WINDOW.blit(SCREW, (scr_x, scr_y))
                #print SCREWS_LIST
                #if distance(Player.x, Player.y, scr_x, scr_y) > 2:
    #print SCREWS


                #elif (scr_x, scr_y) not in SCREWS:
                #    (space_x, space_y) = (char_x, char_y)
                #    if distance(Player.x, Player.y, space_x, space_y) > 2:
                #        WINDOW.blit(SPACE, (space_x, space_y))

            #elif char == char_SPACE:
            #    space_x = char_x
            #    space_y = char_y
            #    AIR.append((space_x, space_y))
            #    if not (Player.x, Player.y) in AIR:
            #        WINDOW.blit(SPACE, (space_x, space_y))
                #if not (Player.x, Player.y) in AIR:
                    #WINDOW.blit(SPACE, (space_x, space_y))
            #WINDOW.blit(EMPTY_SPACE, (Player.x, Player.y))


def draw_map():
    # After setting the (x, y) it's time to draw the characters at those positions

    global level_completed
    global b
    level_completed = True

    for w in WALL_LIST:
        WINDOW.blit(WALL, (w[0], w[1]))

    if distance(Player.x, Player.y, starting_x, starting_y) > 2:
        WINDOW.blit(SPACE, (starting_x, starting_y))

    for s in SCREW_LIST:
        if (s[0], s[1]) in SCREW_LIST:
            if distance(Player.x, Player.y, s[0], s[1]) > 2:
                WINDOW.blit(SCREW, (s[0], s[1]))

    for e in EMPTY_LIST:
        if distance(Player.x, Player.y, e[0], e[1]) > 2:
            WINDOW.blit(SPACE, (e[0], e[1]))

    for sd in SPACE_LIST:
        if distance(Player.x, Player.y, sd[0], sd[1]) > 2:
            WINDOW.blit(SPACE, (sd[0], sd[1]))

        if distance(sd[0], sd[1], BARREL_INSTANCES[0][0].x, BARREL_INSTANCES[0][0].y) > 2:
            WINDOW.blit(BARREL, (BARREL_INSTANCES[0][0].x, BARREL_INSTANCES[0][0].y))
            # i think i have to do a calculation with the changed barre_instances.x, .y

    for b in BARREL_INSTANCES:
        if distance(Player.x, Player.y, b[0].x, b[0].y) > 2: # it is viewing the other list
            WINDOW.blit(BARREL, (b[0].x, b[0].y))

    if level_completed:
        if distance(Player.x, Player.y, st_d_x, st_d_y) > 2:
            WINDOW.blit(STAIR_DOWN, (st_d_x, st_d_y))
        try:
            if distance(Player.x, Player.y, st_u_x, st_u_y) > 2:
                WINDOW.blit(STAIR_UP, (st_u_x, st_u_y))
        except NameError: # did not found stairs up
            pass


def distance(ax, ay, bx, by):
    aa = ax - bx
    bb = ay - by
    c = math.sqrt((aa ** 2) + (bb ** 2))
    return c


def game_logic():
    # what is actually done in steps for the game to be

    # clear
    WINDOW.fill(BLACK)

    # check the current map

    #getcurrent_map()

    # draw character#
    Player.draw(PLAYER)

    # check for gather
    Player.take(SCREW_LIST, EMPTY_LIST)

    # check for push
    Player.push(BARREL_INSTANCES, EMPTY_LIST)

    # draw the map
    draw_map()

    # draw stats
    WINDOW.blit(TEXT, ((25 * char_SIZE - char_SIZE * 25), (25 * char_SIZE + char_SIZE)))

    # update screen
    pygame.display.flip()


#run#

if __name__ == '__main__':
    initialize_game()
    getcurrent_map()
    get_objs()
    print BARREL_INSTANCES
    print BARREL_INSTANCES[4][0].x # ACCESSING INSTANCES
    print BARREL_INSTANCES[4][0].y
    #BARREL_INSTANCES[0][0].x += 1
    #BARREL_INSTANCES[0][0].y += 1
    #draw_map()
    game_loop()
