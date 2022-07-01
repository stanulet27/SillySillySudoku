import random

# generate some funny dictionaries to help keep track of which tiles were
# user filled and help speed up the recursive board creation
userInputted = {}
numberPossibilities = {}
# empty grid
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


# This just is a way to make note of the tiles that are inputted so they are never changed when refacotring the board
def addToUserInputted(tile, number):
    userInputted[tile] = number
    print(userInputted)


# Set the number of possibilities for each tile to be the full 9. These will be lowered as numbers are set
def setNumPossibilities(numberPossibilities_local):
    base = 10
    counter = 1
    for j in range(9):
        for i in range(9):
            tile = (j, i)
            numberPossibilities_local[tile] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        counter += 1


# Sets the tiles that the user filled
def setUserInputted():
    for tile in userInputted:
        column = tile[1]
        row = tile[0]
        grid[row][column] = userInputted[tile]


# Check to see if a "guess" is valid
def isValid(location, value):
    row = location[0]
    col = location[1]
    for c in range(9):  # check row
        if grid[row][c] == value and col != c:
            return False
    for r in range(9):  # check col
        if grid[r][col] == value and row != r:
            return False
    box_x = col // 3  # find block to check
    box_y = row // 3
    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            if grid[r][c] == value and r != row and c != col:
                return False
    return True


# Will subtract the value added as a possibility from its row, column and block
def possibilitySubtractor(location, value):
    for c in range(9):
        if value in numberPossibilities[(location[0], c)]:
            numberPossibilities[(location[0], c)].remove(value)
    for r in range(9):
        if value in numberPossibilities[(r, location[1])]:
            numberPossibilities[(r, location[1])].remove(value)
    # find block to check
    box_x = location[0] // 3
    box_y = location[1] // 3
    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            if value in numberPossibilities[(r, c)]:
                numberPossibilities[(r, c)].remove(value)


# Will check to see if the value can be added back to row, column and block during the backtracking and add if possible
def possibilityAdder(location, value):
    for c in range(9):
        if isValid((location[0], c), value):
            numberPossibilities[(location[0], c)].append(value)
    for r in range(9):
        if isValid((r, location[1]), value):
            numberPossibilities[(r, location[1])].append(value)
    # find block to check
    box_x = location[0] // 3
    box_y = location[1] // 3
    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            if isValid((r, c), value):
                numberPossibilities[(r, c)].append(value)


# A recursive function to create a game board around the user inputted tiles
def boardCreator():
    # base: when having an empty board, set a random tile to begin the process
    if len(userInputted) == 0:
        val = random.randint(1, 10)
        location = (random.randint(1, 10), random.randint(1, 10))
        grid[location[0]][location[1]] = val
        possibilitySubtractor(location, val)

    lowestPossKey = min(numberPossibilities, key=numberPossibilities.get)

    # if the board is not complete, recur to get another cell filled
    if any(0 in sublist for sublist in grid):
        boardCreator()


# put it all together now! :)
def build():
    # initialize list of the possibilities for each
    setNumPossibilities(numberPossibilities)
    # first thing is to set the user inputted tiles (this will be empty at first)
    setUserInputted()
    # next step is to find a possible game board
    boardCreator()
    # last step is to remove a few of the computer generated tiles to actually make it a puzzle

    # return the grid to the main game file
    return grid
