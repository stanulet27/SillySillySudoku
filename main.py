import pygame
import GameBuilder
from pygame.locals import *
from sys import exit
import random

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

# get grid
grid = GameBuilder.build()


def fillTile(selected, location, keyPressed, grid_local):
    #if selected:
    GameBuilder.addToUserInputted(location, keyPressed)
    #grid_local = GameBuilder.build()



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
                    text_surface = font.render(str(grid[row][col]), False, (0, 0, 0))
                    display.blit(text_surface, [(row * TILE_SIZE) + 10, (col * TILE_SIZE) + 8])
        pygame.display.update()


print("board is ready")
drawBoard()

selected = False
click_x = 0
click_y = 0
while True:  # THIS IS WHERE THE GAME LOOP STARTS !!!!!!!!!

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # find cell that was clicked then use the mouse coordinates to "select" one
            pos = pygame.mouse.get_pos()
            # find the block that was pressed and store it as a tuple
            location = (pos[1] // TILE_SIZE, pos[0] // TILE_SIZE)

            print(location)
            selected = True
        elif event.type == KEYDOWN:  # basically enter the number that was pressed ik this is probably super inefficient
                keyPressed = event.__getattribute__('unicode')
                fillTile(selected, location, keyPressed, grid)
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
            break

