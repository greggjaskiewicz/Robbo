#!/usr/bin/python

import pygame
import math

####constants####
WIDTH = 373 # 800 adjusted for map 25x25: 373
HEIGHT = 405 # 600 adjusted for map 25x25: 405
#colors#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
BROWN = (102, 51, 0)
ROBBO_GREEN = (0, 150, 0)
RED = (255, 0, 0)
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
# TODO MAKE A CLASS FOR EVERY OBJECT

class PlayerClass: # will be the player and the barrel

    def __init__(self, x, y, hp=None, screws=None):
        self.x = x
        self.y = y
        self.hp = hp
        self.screws = screws

    def move(self, dx, dy):
        if not (self.x + dx, self.y + dy) in WALL_LIST: # and Barrel.x .y (BARREL_INSTANCES(PUSHABLE_LIST))
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

    def push(self, pushable_list, dx, dy):
        #CHANGED_BARRELS_LIST.append((pushable_list[0][0].x, pushable_list[0][0].y))
        global CHANGING_PUSHABLE_LIST
        CHANGING_PUSHABLE_LIST = unpack_INSTANCES(pushable_list)
        for p1 in pushable_list:
            dir_x = p1[0].x + dx
            dir_y = p1[0].y + dy
            if distance(p1[0].x, p1[0].y, self.x, self.y) < 2:
                if not (dir_x, dir_y) in WALL_LIST:
                    if (dir_x, dir_y) in CHANGING_PUSHABLE_LIST:
                        self.move(-dx, -dy)
                    else:
                        p1[0].x += dx
                        p1[0].y += dy
                else:
                    self.move(-dx, -dy)

            #if distance(p1[0].x, p1[0].y, self.x, self.y) < 2:
            #    p1[0].x += 15

        #for p1 in pushable_list:
        #    for p2 in pushable_list:
        #        if distance(p1[0].x, p1[0].y, self.x, self.y) < 2:
        #            if distance(p1[0].x, p1[0].y, p2[0].x, p2[0].y) > 2:
        #                p1[0].x += 15

                #if distance(p1[0].x, p1[0].y, p1[0].x, p1[0].y) < 2:
                #    print 'd'
            #if distance(p1[0].x, p1[0].y, p1[0].x, p1[0].y) < 2:
            #    if distance(p1[0].x, p1[0].y, self.x, self.y) > 2:
            #        if (p1[0].x + char_SIZE, p1[0].y + char_SIZE) in SPACE_LIST:
            #            print p1[0].x, p1[0].y
            #            bin.append((p1[0].x, p[0].y))
            #            p1[0].x += 15


class BarrelClass:

    global barrels

    def __init__(self, x, y):
        self.x = x
        self.y = y
        global barrels
        barrels = [self.x, self.y]

    def draw(self, icon):
        WINDOW.blit(icon, (self.x, self.y))

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
                    Player.push(BARREL_INSTANCES, 0, -15)
                elif event.key == pygame.K_DOWN:
                    Player.move(0, 15)
                    Player.push(BARREL_INSTANCES, 0, 15)
                elif event.key == pygame.K_LEFT:
                    Player.move(-15, 0)
                    Player.push(BARREL_INSTANCES, -15, 0)
                elif event.key == pygame.K_RIGHT:
                    Player.move(15, 0)
                    Player.push(BARREL_INSTANCES, 15, 0)
                elif event.key == pygame.K_d:
                    #descend = True # change map descent not present in this version
                    # TODO MAKE MULTIPLE LEVELS, WITH STAIRS JUST FOR THE SAKE OF IT
                    pass

        if not game_won:
            game_logic()
        else:
            victory_screen()

def initialize_game():

    global WINDOW
    global FONT
    global PLAYER
    global WALL
    global SPACE
    global EMPTY_SPACE
    global STAIR_DOWN
    global STAIR_UP
    global SCREW
    global BARREL
    global STATS
    global VERSION

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
    STATS = FONT.render("HP:{0} Screws:{1} Level:{2}".format(Player.hp, Player.screws, current_level_number), 0, WHITE)
    VERSION = FONT.render("v.1.0", 0, RED)

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
    global current_level_number
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
    global CHANGING_PUSHABLE_LIST
    global SCREWS

    SCREWS = 0
    CHANGING_PUSHABLE_LIST = []
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
                SCREWS += 1
                SCREW_LIST.append((scr_x, scr_y))

            elif char == char_EMPTY:
                (e_x, e_y) = (char_x, char_y)
                EMPTY_LIST.append((e_x, e_y))

            elif char == char_BARREL:
                (b_x, b_y) = (char_x, char_y) # starting position of the barrels
                #for b in char:
                Barrel = BarrelClass(b_x, b_y)
                BARREL_INSTANCES.append([Barrel])
                BARREL_LIST.append((b_x, b_y))
                EMPTY_LIST.append((b_x, b_y))
                #print BARREL_INSTANCES[0][0].x, BARREL_INSTANCES[0][0].y



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

        #if distance(sd[0], sd[1], BARREL_INSTANCES[0][0].x, BARREL_INSTANCES[0][0].y) > 2:
        #    WINDOW.blit(BARREL, (BARREL_INSTANCES[0][0].x, BARREL_INSTANCES[0][0].y))
            # i think i have to do a calculation with the changed barrel_instances.x, .y

    for b in BARREL_INSTANCES:
        if distance(Player.x, Player.y, b[0].x, b[0].y) > 2:
            WINDOW.blit(BARREL, (b[0].x, b[0].y))

    if level_completed:
        if distance(Player.x, Player.y, st_d_x, st_d_y) > 2:
            WINDOW.blit(STAIR_DOWN, (st_d_x, st_d_y))
        try:
            if distance(Player.x, Player.y, st_u_x, st_u_y) > 2:
                WINDOW.blit(STAIR_UP, (st_u_x, st_u_y))
        except NameError: # did not found stairs up
            pass


def draw_stats():
    STATS = FONT.render("HP:{0} Screws:{1} Level:{2}".format(Player.hp, Player.screws, current_level_number), 0, WHITE)
    WINDOW.blit(STATS, ((25 * char_SIZE - char_SIZE * 25), (25 * char_SIZE + char_SIZE)))

def draw_version():
    WINDOW.blit(VERSION, (WIDTH - char_SIZE * 5, HEIGHT - char_SIZE))

def distance(ax, ay, bx, by):
    aa = ax - bx
    bb = ay - by
    c = math.sqrt((aa ** 2) + (bb ** 2))
    return c

def unpack_INSTANCES(package):
    list = []
    for l in package:
        list.append((l[0].x, l[0].y))
    return list

def check_for_win():
    if Player.screws == SCREWS:
        return True

def game_logic():
    global game_won
    # what is actually done in steps for the game to be

    # clear
    WINDOW.fill(BLACK)

    # check the current map

    #getcurrent_map()

    # draw character#
    Player.draw(PLAYER)

    # check for gather
    Player.take(SCREW_LIST, EMPTY_LIST)

    # draw the map
    draw_map()

    # draw stats
    draw_stats()

    # check for win

    game_won = check_for_win()

    # update screen
    pygame.display.flip()


#run#

def victory_screen():
    WINDOW.fill(BLACK)
    WON = FONT.render('YOU HAVE GATHERED', 0, WHITE)
    WON2 = FONT.render('ALL THE SCREWES :DDD', 0 , WHITE)
    WINDOW.blit(WON, (WIDTH / 2 - 130, HEIGHT / 2 - 15))
    WINDOW.blit(WON2, (WIDTH / 2 - 150, HEIGHT / 2))
    draw_version()
    pygame.display.flip()

if __name__ == '__main__':
    game_won = False
    initialize_game()
    getcurrent_map()
    get_objs()
    #print BARREL_INSTANCES
    #print BARREL_INSTANCES[4][0].y
    #for p in BARREL_INSTANCES:
    #    print p[0].y
    #BARREL_INSTANCES[0][0].x += 1
    #BARREL_INSTANCES[0][0].y += 1
    #print BARREL_LIST
    #draw_map()
    #print barrels
    game_loop()
