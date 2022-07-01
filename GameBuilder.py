import random

# generare some funny dictionaries to help keep track of which tiles were
# user filled and help speed up the recursive board creation
userinputted = {}
numberPossibilites = {}
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
    userinputted[tile] = number
    print(userinputted)


# Set the number of possibilities for each tile to be the full 9. These will be lowered as numbers are set
def setNumPossibilities(numberPossibilites_local):
    base = 10
    counter = 1
    for j in range(9):
        for i in range(9):
            tile = (j, i)
            numberPossibilites_local[tile] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        counter += 1


# Sets the tiles that the user filled
def setUserInputted():
    for tile in userinputted:
        column = tile[1]
        row = tile[0]
        grid[row][column] = userinputted[tile]


# Check to see if a "guess" is valid
def isValid(num, row, col):
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


# Adjusts the number of possible values for a tile. addOrSubtract will be a boolean value: true = subtract, false = add
def possibilityAdjuster(location, value, subtract):
    if subtract:
        for c in range(9):
            if value in numberPossibilites[(location[0],c)]:
                numberPossibilites[(location[0],c)].remove(value)
        for r in range(9):
            if value in numberPossibilites[(r, location[1])]:
                numberPossibilites[(r, location[1])].remove(value)


# A recursive function to create a game board around the user inputted tiles
def boardCreator():
    # base: when having an empty board, set a random tile to begin the process
    if len(userinputted) == 0:
        val = random.randint(1, 10)
        location =(random.randint(1, 10), random.randint(1, 10))
        grid[location[0]][location[1]] = val
        possibilityAdjuster(location, val, True)

    lowestPossKey = min(numberPossibilites, key=numberPossibilites.get)

    # if the board is not complete, recur to get another cell filled
    if any(0 in sublist for sublist in grid):
        boardCreator()



# put it all together now! :)
def build():
    # initialize list of the possibilities for each
    setNumPossibilities(numberPossibilites)
    # first thing is to set the user inputted tiles (this will be empty at first)
    setUserInputted()
    # next step is to find a possible game board
    boardCreator()
    # last step is to remove a few of the computer generated tiles to actually make it a puzzle

    # return the grid to the main game file
    return grid
