import pygame
import random

####constants####
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ROBBO_GREEN = (0, 150, 0)
char_PLAYER = '@'
char_WALL = '#'
char_SPACE = '.'
################

#classes#



#GAME#

def game_loop():
    global game_QUIT

    game_QUIT = False

    while not game_QUIT:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                game_QUIT = True

def initialize_game():

    global WINDOW
    global PLAYER
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont('px437ati8x8', 10)
    PLAYER = FONT.render(char_PLAYER, 0, WHITE)
    #f = pygame.font.get_fonts()
    #print f

    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

def get_map(): # returns file
    pass

def get_objs(): # gets everything on a map
    pass
#DRAWING#

def draw_map(): # draws the map from a file
    pass

def draw_game():

    global WINDOW

    # clear
    WINDOW.fill(BLACK)

    # draw the map

    draw_map()

    # draw character
    WINDOW.blit(PLAYER, (WIDTH / 2, HEIGHT / 2)) # p_x, p_y

    # update screen
    pygame.display.flip()



#run#
if __name__ == '__main__':
    initialize_game()
    draw_game()
    game_loop()