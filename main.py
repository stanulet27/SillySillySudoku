import pygame
from pygame.locals import *
import random
import time

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
# initialise empty 9 by 9 grid
grid = [
    [5, 1, 9, 6, 8, 7, 4, 3, 2],
    [7, 2, 4, 9, 1, 3, 6, 5, 8],
    [3, 8, 6, 2, 5, 4, 9, 1, 7],
    [1, 7, 8, 3, 4, 5, 2, 9, 6],
    [6, 5, 2, 8, 9, 1, 7, 4, 3],
    [9, 4, 3, 7, 2, 6, 5, 8, 1],
    [2, 3, 1, 4, 7, 9, 8, 6, 5],
    [4, 6, 7, 5, 3, 8, 1, 2, 9],
    [8, 9, 5, 1, 6, 2, 3, 7, 4],
]


def digginHelper(board, list_of_removed_spaces,counter ):
    for i in list_of_removed_spaces:
        board[i[0]][i[1]] = 0
    return board

def digging(board):
    list_of_removed_spaces = []
    attempts = 0
    while attempts <= 60 :
        # Select a random cell that is not already empty
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        # Remember its cell value in case we need to put it back
        backup = board[row][col]
        board[row][col] = 0
        list_of_removed_spaces.append([row,col])
        board = digginHelper(board, list_of_removed_spaces, attempts)
        attempts += 1
        # drawBoard(board)
        if not solve_sudoku(board):
            board[row][col] = backup
            list_of_removed_spaces.remove(len(list_of_removed_spaces - 1))
            attempts -=1
    digginHelper(board,list_of_removed_spaces,attempts)
    return board


def shuffle(board):
    # row group 1
    board = row_swapper(0, grid[0], grid[1], grid[2], board)
    # row group 2
    board = row_swapper(1, grid[3], grid[4], grid[5], board)
    # row group 3
    board = row_swapper(2, grid[6], grid[7], grid[8], board)
    # groups
    board = group_swapper([board[0], board[1], board[2]], [board[3], board[4], board[5]], [board[6], board[7], board[8]], board)
    return board


def row_swapper(groupNum, row1, row2, row3, board):
    random_list = [row1, row2, row3]
    random.shuffle(random_list)
    i = groupNum * 3
    board[i] = random_list[0]
    board[i + 1] = random_list[1]
    board[i + 2] = random_list[2]
    return board


def group_swapper(group1, group2, group3, board):
    random_groups = [group1, group2, group3]
    random.shuffle(random_groups)
    board[0] = random_groups[0][0]
    board[1] = random_groups[0][1]
    board[2] = random_groups[0][2]
    board[3] = random_groups[1][0]
    board[4] = random_groups[1][1]
    board[5] = random_groups[1][2]
    board[6] = random_groups[2][0]
    board[7] = random_groups[2][1]
    board[8] = random_groups[2][2]
    return board

    pass


def solve_sudoku(puzzle):
    row, column = find_next_empty(puzzle)
    if row is None:  # check to see if grid is full
        return True
    for guess in range(1, 10):
        if valid(guess, row, column):
            puzzle[row][column] = guess
            if solve_sudoku(puzzle):
                return True
            puzzle[row][column] = 0
    return False


def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None, None


def valid(num, row, col):
    for c in range(9):  # check row
        if grid[row][c] == num and col != c:
            return False
    for r in range(9):  # check col
        if grid[r][col] == num and row != r:
            return False
    box_x = col // 3  # find block to check
    box_y = row // 3
    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            if grid[r][c] == num and r != row and c != col:
                return False
    return True


def drawBoard(board):

    display.fill((255,255,255))
    for i in range(9): # draw vertical lines
        if i % 3 ==0:
            pygame.draw.line(display, (0,0,0), ((TILE_SIZE*i), 0), ((TILE_SIZE*i),(TILE_SIZE*9)),2)
        else:
            pygame.draw.line(display, (0,0,0), ((TILE_SIZE*i), 0), ((TILE_SIZE*i),(TILE_SIZE*9)),1)
        for i in range(9): # draw vertical lines
            if i % 3 ==0:
                pygame.draw.line(display, (0,0,0), (0,(TILE_SIZE*i)), ((TILE_SIZE*9),(TILE_SIZE*i)),2)
            else:
                pygame.draw.line(display, (0,0,0), (0, (TILE_SIZE*i)), ((TILE_SIZE*9),(TILE_SIZE*i)),1)
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:  # insert number into corresponding block. ignore 0's they're empty spots
                    text_surface = font.render(str(board[row][col]), False, (0, 0, 0))
                    display.blit(text_surface,[(row * TILE_SIZE) +10 , (col * TILE_SIZE)+8 ])
        pygame.display.update()

def checkWin(board):
    for r in range(9):
        for c in range(9):
            if not valid(board[r][c], r, c):
                print("answer is not valid")
                return False
            else:
                print("answer is valid")


grid = shuffle(grid)
drawBoard(grid)
checkWin(grid)
playing_board = digging(grid)
drawBoard(playing_board)


print("board is ready")
selected = False
click_x = 0
click_y = 0
while True:  # THIS IS WHERE THE GAME LOOP STARTS !!!!!!!!!
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:  # find cell that was clicked then use the mouse coordinates to
            # "select" one
            pos = pygame.mouse.get_pos()
            click_x = pos[0] // (TILE_SIZE)  # find the block that was pressed
            click_y = pos[1] // (TILE_SIZE)
            print(click_x, click_y)
            selected = True
        elif event.type == KEYDOWN:  # basically enter the number that was pressed ik this is probably super inefficient
            if event.key == K_1:
                if selected and playing_board[click_x][click_y] == 0:
                    playing_board[click_x][click_y] = 1
                    selected = False
                    drawBoard(playing_board)
            elif event.key == K_2:
                if selected:
                    playing_board[click_x][click_y] = 2
                    selected = False
                    drawBoard(playing_board)
            elif event.key == pygame.K_3:
                if selected:
                    playing_board[click_x][click_y] = 3
                    selected = False
                    drawBoard(playing_board)
            elif event.key == pygame.K_4:
                if selected:
                    playing_board[click_x][click_y] = 4
                    selected = False
                    drawBoard(playing_board)
            elif event.key == pygame.K_5:
                if selected:
                    playing_board[click_x][click_y] = 5
                    selected = False
                    drawBoard(playing_board)
            elif event.key == pygame.K_6:
                if selected:
                    playing_board[click_x][click_y] = 6
                    selected = False
                    drawBoard(playing_board)
            elif event.key == pygame.K_7:
                if selected:
                    playing_board[click_x][click_y] = 7
                    selected = False
                    drawBoard(playing_board)
            elif event.key == pygame.K_8:
                if selected:
                    playing_board[click_x][click_y] = 8
                    selected = False
                    drawBoard(playing_board)
            elif event.key == pygame.K_9:
                if selected:
                    playing_board[click_x][click_y] = 9
                    selected = False
                    drawBoard(playing_board)
