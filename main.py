import pygame
from Board import Board
from pygame.locals import *
from sys import exit


# Game variables
TILE_SIZE = 32
BLOCK_WIDTH = 30
MARGIN = 2
WIN_WIDTH = TILE_SIZE * 9
WIN_HEIGHT = TILE_SIZE * 9
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('calibri', 22)
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
display.fill((0, 0, 0))
pygame.display.set_caption("Sudoku")

#get grid

#this will be the main grid
grid = Board()
print("getting grid")

def drawBoard():

    display.fill((255, 255, 255))
    for i in range(9):  # draw horizontal lines
        if i % 3 == 0:
            pygame.draw.line(display, (0, 0, 0), ((TILE_SIZE * i), 0), ((TILE_SIZE * i), (TILE_SIZE * 9)), 2)
        else:
            pygame.draw.line(display, (0, 0, 0), ((TILE_SIZE * i), 0), ((TILE_SIZE * i), (TILE_SIZE * 9)), 1)
    for i in range(9):  # draw vertical lines
        if i % 3 == 0:
            pygame.draw.line(display, (0, 0, 0), (0, (TILE_SIZE * i)), ((TILE_SIZE * 9), (TILE_SIZE * i)), 2)
        else:
            pygame.draw.line(display, (0, 0, 0), (0, (TILE_SIZE * i)), ((TILE_SIZE * 9), (TILE_SIZE * i)), 1)
    for row in range(9):
        for col in range(9):

            if grid[row][col] != 0:  # insert number into corresponding block. ignore 0's they're empty spots
                color = 0
                if grid.user[row][col] !=0:
                    color = 255
                text_surface = font.render(str(grid[row][col]), False, (0, 0, color))
                # coords are (x,y) which is (col, row)
                display.blit(text_surface, [(col * TILE_SIZE) + 10, (row * TILE_SIZE) + 8])
    pygame.display.update()



drawBoard()

selected = False
click_x = 0
click_y = 0
while True:  # THIS IS WHERE THE GAME LOOP STARTS !!!!!!!!!


    for event in pygame.event.get():
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # find cell that was clicked then use the mouse coordinates to "select" one
            pos = pygame.mouse.get_pos()
            # find the block that was pressed and store it as a tuple
            ###location is stored as (row, col)###
            location = (pos[1] // TILE_SIZE, pos[0] // TILE_SIZE)
            print(location)
        elif event.type == KEYDOWN:  # enter the number that was pressed 
            keyPressed = event.__getattribute__('unicode')

            if(keyPressed != '\b'):
                if grid.enterSpace(location,int(keyPressed)):
                    drawBoard()
                else:
                    text_surface = font.render(keyPressed, False, (255, 0, 0))
                    display.blit(text_surface, [(location[1] * TILE_SIZE) + 10, (location[0] * TILE_SIZE) + 8])
            else:
                drawBoard()

        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

