import pygame
import random
import math

####constants####
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ROBBO_GREEN = (0, 150, 0)
char_PLAYER = '@'
char_WALL = '#'
char_SPACE = '.'
char_EMPTY = ' '
char_STAIR_DOWN = '>'
char_STAIR_UP = '<'
char_SIZE = 10
current_level = []
current_level_number = 1
################

#classes#

class Tile:

    def __init__(self, block_path):
        self.block_path = block_path


class Obj: # will be the player and the barrel

    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp

    def move(self, dx, dy):
        if not (self.x + dx, self.y + dy) in blocked:
            self.x += dx
            self.y += dy


#GAME#

def game_loop():
    global game_QUIT

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
                    Player.move(0, -10)
                elif event.key == pygame.K_DOWN:
                    Player.move(0, 10)
                elif event.key == pygame.K_LEFT:
                    Player.move(-10, 0)
                elif event.key == pygame.K_RIGHT:
                    Player.move(10, 0)

        draw_game()

def initialize_game():

    global WINDOW
    global PLAYER
    global WALL
    global SPACE
    global EMPTY_SPACE
    global STAIR_DOWN
    global STAIR_UP

    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont('px437ati8x8', char_SIZE)
    PLAYER = FONT.render(char_PLAYER, 0, ROBBO_GREEN)
    WALL = FONT.render(char_WALL, 0, WHITE)
    SPACE = FONT.render(char_SPACE, 0, WHITE)
    EMPTY_SPACE = FONT.render(char_EMPTY, 0, WHITE)
    STAIR_DOWN = FONT.render(char_STAIR_DOWN, 0, WHITE)
    STAIR_UP = FONT.render(char_STAIR_UP, 0 , WHITE)

    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

def get_map(): # returns file
    global current_level
    current_level = []
    levels = []
    with open('level_%s.txt' % current_level_number, 'r') as l_map:
        for line in l_map:
            current_level.append(line)
    return current_level

def get_character():
    lvl = get_map()
    for y in range(len(lvl)):
        for x in range(len(lvl[y])):
            char = lvl[y][x]

            char_x = 0 + (x * char_SIZE)
            char_y = 0 + (y * char_SIZE)

            if char == char_PLAYER:
                player_x, player_y = (char_x, char_y)
                return player_x, player_y

player_x, player_y = get_character()
Player = Obj(player_x, player_y, 100)

#DRAWING#

def draw_map(): # draws the map from a file
    global blocked
    global AIR
    global space_x
    global space_y
    blocked = []
    AIR = []
    level = get_map()
    for y in range(len(level)):
        for x in range(len(level[y])):
            char = level[y][x]

            char_x = 0 + (x * char_SIZE)
            char_y = 0 + (y * char_SIZE)
            # TODO use get_objects and use for loop to draw objects

            if char == char_WALL:
                wall_x, wall_y = (char_x, char_y)
                blocked.append((wall_x, wall_y))
                WINDOW.blit(WALL, (wall_x, wall_y))

            elif char == char_PLAYER:
                (starting_x, starting_y) = (char_x, char_y)
                if distance(Player.x, Player.y, starting_x, starting_y) > 2:
                    WINDOW.blit(SPACE, (starting_x, starting_y))

            elif char == char_SPACE:
                (space_x, space_y) = (char_x, char_y)
                if distance(Player.x, Player.y, space_x, space_y) > 2:
                    WINDOW.blit(SPACE, (space_x, space_y))

            elif char == char_STAIR_DOWN:
                (st_d_x, st_d_y) = (char_x, char_y)
                if distance(Player.x, Player.y, st_d_x, st_d_y) > 2:
                    WINDOW.blit(STAIR_DOWN, (st_d_x, st_d_y))

            elif char == char_STAIR_UP:
                (st_u_x, st_u_y) = (char_x, char_y)
                if distance(Player.x, Player.y, st_u_x, st_u_y) > 2:
                    WINDOW.blit(STAIR_DOWN, (st_u_x, st_u_y))



            #elif char == char_SPACE:
            #    space_x = char_x
            #    space_y = char_y
            #    AIR.append((space_x, space_y))
            #    if not (Player.x, Player.y) in AIR:
            #        WINDOW.blit(SPACE, (space_x, space_y))
                #if not (Player.x, Player.y) in AIR:
                    #WINDOW.blit(SPACE, (space_x, space_y))
            #WINDOW.blit(EMPTY_SPACE, (Player.x, Player.y))


def distance(ax, ay, bx, by):
    aa = ax - bx
    bb = ay - by
    c = math.sqrt((aa ** 2) + (bb ** 2))
    return c

def draw_space():
    p1 = [x not in AIR for x in (Player.x, Player.y)]
    p2 = [y not in AIR[x] for y in (Player.x, Player.y)]
    print x

def draw_character():
    WINDOW.blit(PLAYER, (Player.x, Player.y))

def draw_game():

    global WINDOW

    # clear
    WINDOW.fill(BLACK)

    # draw the map

    draw_map()
    # draw character#

    draw_character()

    # update screen
    pygame.display.flip()


#run#

if __name__ == '__main__':
    initialize_game()
    game_loop()

