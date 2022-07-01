import random

# generate some funny dictionaries to help keep track of which tiles were
# user filled and help speed up the recursive board creation
userInputted = {}
listOfPossibilities = {}
numPossibilities = {}
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
def setNumPossibilities(listOfPossibilities_local, numberPossibilities_local):
    base = 10
    counter = 1
    for j in range(9):
        for i in range(9):
            tile = (j, i)
            listOfPossibilities_local[tile] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            numberPossibilities_local[tile] = 9
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
        if value in listOfPossibilities[(location[0], c)]:
            listOfPossibilities[(location[0], c)].remove(value)
            numPossibilities[(location[0], c)] = len(listOfPossibilities[(location[0], c)])
    for r in range(9):
        if value in listOfPossibilities[(r, location[1])]:
            listOfPossibilities[(r, location[1])].remove(value)
            numPossibilities[(r, location[1])] = len(listOfPossibilities[(r, location[1])])
    # find block to check
    box_x = location[0] // 3
    box_y = location[1] // 3
    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            if value in listOfPossibilities[(r, c)]:
                listOfPossibilities[(r, c)].remove(value)
                numPossibilities[(r, c)] = len(listOfPossibilities[(r, c)])
    # set the number of possibilities of the filled tiles to 10 10's. This way we can still use the min function
    # while skipping the filled tiles
    listOfPossibilities[location] = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    numPossibilities[location] = 10


# Will check to see if the value can be added back to row, column and block during the backtracking and add if possible
def possibilityAdder(location):
    for c in range(9):
        for value in range(9):
            if isValid((location[0], c), value):
                listOfPossibilities[(location[0], c)].append(value)
        numPossibilities[(location[0], c)] = len(listOfPossibilities[(location[0], c)])
    for r in range(9):
        for value in range(9):
            if isValid((r, location[1]), value):
                listOfPossibilities[(r, location[1])].append(value)
        numPossibilities[(r, location[1])] = len(listOfPossibilities[(r, location[1])])
    # find block to check
    box_x = location[0] // 3
    box_y = location[1] // 3
    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            for value in range(9):
                if isValid((r, c), value):
                    listOfPossibilities[(r, c)].append(value)
        numPossibilities[(r, c)] = len(listOfPossibilities[(r, c)])


# A recursive function to create a game board around the user inputted tiles
def boardCreator():
    # check if solved to break out
    if not any(0 in sublist for sublist in grid):
        return True

    # get the tile with the lowest number of possbilities
    lowestPossKey = min(listOfPossibilities, key=listOfPossibilities.get)
    # get list of possible values
    possibilities = listOfPossibilities[lowestPossKey]

    # before I start setting stuff I want to see if there is a black space with no possibilities
    # if there is then we can skip the whole part where we set things and just backtrack

    # if there is a tile with zero possibilities then the creation has reached a dead end, backtrack
    if len(possibilities) != 0:
        # get random value from that list
        val = possibilities[random.randint(0, len(possibilities) - 1)]
        # set the tile to that random value
        column = lowestPossKey[1]
        row = lowestPossKey[0]
        grid[row][column] = val
        # remove possibility from that tile
        possibilitySubtractor(lowestPossKey, val)

        # if the board is not complete, recur to get another cell filled
        if boardCreator():
            return True

        # if the code is reading this then we have a problem, backtrack
        grid[lowestPossKey[0]][lowestPossKey[1]] = 0
        possibilityAdder(lowestPossKey)


# put it all together now! :)
def build():
    # initialize list of the possibilities for each
    setNumPossibilities(listOfPossibilities, numPossibilities)
    # first thing is to set the user inputted tiles (this will be empty at first)
    setUserInputted()

    # base: when having an empty board, set a random tile to begin the process
    if len(userInputted) == 0:
        val = random.randint(1, 9)
        randX = random.randint(0, 8)
        randY = random.randint(0, 8)
        grid[randX][randY] = val
        possibilitySubtractor((randX, randY), val)

    # next step is to find a possible game board
    boardCreator()
    # last step is to remove a few of the computer generated tiles to actually make it a puzzle

    # return the grid to the main game file
    return grid
