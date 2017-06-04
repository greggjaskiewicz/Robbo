import pygame
import math

####constants####
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
ROBBO_GREEN = (0, 150, 0)
char_PLAYER = '@'
char_WALL = '#'
char_SPACE = '.'
char_EMPTY = ' '
char_STAIR_DOWN = '>' # when going to the next level, offload the status of current level to a new file, and then read that updated file
char_STAIR_UP = '<'
char_SCREW = '*'
char_SIZE = 15
MAX_NUMBER_LEVELS = 2
#LEVEL_NUM = 2
################

#classes#

class Obj: # will be the player and the barrel

    def __init__(self, x, y, hp, screws):
        self.x = x
        self.y = y
        self.hp = hp
        self.screws = screws

    def move(self, dx, dy):
        if not (self.x + dx, self.y + dy) in WALLS_LIST:
            self.x += dx
            self.y += dy

    def take(self, gathering_list, bin):
        try:
            for g in gathering_list:
                if distance(Player.x, Player.y, g[0], g[1]) < 2:
                    gathering_list.remove((g[0], g[1]))
                    bin.append((g[0], g[1]))
                    self.screws += 1
        except ValueError:
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

def get_screw():
    # ex. [[120, 75], [105, 90], [120, 90], [60, 180], [180, 180], [60, 225], [180, 225]]
    for s in SCREWS_LIST:
        print s[0], s[1]
        if distance(Player.x, Player.y, s[0], s[1]) < 2:
            return s[0], s[1]

def get_obj(char_obj):
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
Player = Obj(player_x, player_y, 100, 0)

#DRAWING#

def get_objs():
    # The only aim for this function is to set position to every defined character on screen

    # THIS IS GETTING AND LOOPING FOREVER THE LISTS, THIS HAS TO BE DONE OUTSIDE THE LOOP!!! < - Done
    # commented blocks are my mistakes

    global WALLS_LIST
    global AIR
    global space_x, space_y
    global starting_x, starting_y
    global wall_x, wall_y
    global st_d_x, st_d_y
    global st_u_x, st_u_y
    global scr_x, scr_y
    global SCREWS_LIST
    global SPACE_LIST
    global EMPTY_LIST

    EMPTY_LIST = []
    WALLS_LIST = []
    SCREWS_LIST = []
    SPACE_LIST = []
    level = current_level
    for y in range(len(level)):
        for x in range(len(level[y])):
            char = level[y][x]

            char_x = 0 + (x * char_SIZE)
            char_y = 0 + (y * char_SIZE)
            # TODO use get_objects and use for loop to draw objects

            if char == char_WALL:
                wall_x, wall_y = (char_x, char_y)
                WALLS_LIST.append((wall_x, wall_y))
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
                SCREWS_LIST.append((scr_x, scr_y))
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
    level_completed = True

    for w in WALLS_LIST:
        WINDOW.blit(WALL, (w[0], w[1]))

    if distance(Player.x, Player.y, starting_x, starting_y) > 2:
        WINDOW.blit(SPACE, (starting_x, starting_y))

    for s in SCREWS_LIST:
        if (s[0], s[1]) in SCREWS_LIST:
            if distance(Player.x, Player.y, s[0], s[1]) > 2:
                WINDOW.blit(SCREW, (s[0], s[1]))

    for e in EMPTY_LIST:
        if distance(Player.x, Player.y, e[0], e[1]) > 2:
            WINDOW.blit(SPACE, (e[0], e[1]))

    for sd in SPACE_LIST:
        if distance(Player.x, Player.y, sd[0], sd[1]) > 2:
            WINDOW.blit(SPACE, (sd[0], sd[1]))

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

def draw_character():
    WINDOW.blit(PLAYER, (Player.x, Player.y))

def game_logic():
    # what is actually done in steps for the game to be

    # clear
    WINDOW.fill(BLACK)

    # check the current map

    #getcurrent_map()

    # draw character#
    draw_character()

    # check for gather
    Player.take(SCREWS_LIST, EMPTY_LIST)

    # draw the map
    draw_map()

    # update screen
    pygame.display.flip()


#run#

if __name__ == '__main__':
    initialize_game()
    getcurrent_map()
    get_objs()
    #draw_map()
    game_loop()
