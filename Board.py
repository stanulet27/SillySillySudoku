import random
import copy

class Board:
    def __init__(self,board_string=None):
        #creates a new, empty board
        self.__resetBoard()
        #if not null it will fill in the board with what was passed in the solve to get new key
        if board_string:
            self.board_string = board_string
            for row in range(9):
                for col in range(9):
                    self.board[row][col] = int(board_string[0])
                    board_string = board_string[1:]
        # if null then generate a random board
        else:
            self.__generateRamdomBoard()
            self.board_string = self.boardToboard_string()


    def __getitem__(self,key):
        return self.board[key]

    def __resetBoard(self):
        self.board = [
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
        return self.board

    def boardToboard_string(self, input_board=None):
        #returns stirng for other board
        if input_board:
            _board_string = ''.join([str(i) for j in input_board for i in j])
            return _board_string
        #returns the string for this board instance
        else:
            self.board_string = ''.join([str(i) for j in self.board for i in j])
            return self.board_string 

    def findFirstEmpty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row,col)
        return False
    
    def isValid(self,num,space):
        #make sure space is empty
        if not self.board[space[0]][space[1]] == 0:
            return False
        #make sure num is not in col
        for col in self.board[space[0]]:
            if col == num:
                return False
        #make sure num is not in row
        for row in range(len(self.board)):
            if self.board[row][space[1]] == num:
                return False

        boxR = space[0] // 3
        boxC = space[1] // 3
        #make sure num is not in the same 3x3 'box'
        for i in range(3):
            for j in range(3):
                if self.board[i + (boxR * 3)][j + (boxC * 3)] == num:
                    return False

        #if you've made it here, its a valid guess so far!
        return True

    def solve(self):
        spacesAvailable = self.findFirstEmpty()
        if not spacesAvailable:
            return True
        else:
            row,col = spacesAvailable
        
        for n in range (1,10):
            if self.isValid(n,(row,col)):
                self.board[row][col] = n
                if self.solve():
                    return True
            
            self.board[row][col] = 0

        return False

    def __generateRamdomBoard(self):
        #generate fill top left block randomly
        _nums = list(range(1,10))
        for row in range(3):
            for col in range(3):
                _num = random.choice(_nums)
                self.board[row][col] = _num
                _nums.remove(_num)
        #same for center block
        _nums = list(range(1,10))        
        for row in range(3,6):
            for col in range(3,6):
                _num = random.choice(_nums)
                self.board[row][col] = _num
                _nums.remove(_num)

        #same for bottom left
        _nums = list(range(1,10))
        for row in range(6,9):
            for col in range(6,9):
                _num = random.choice(_nums)
                self.board[row][col] = _num
                _nums.remove(_num)
        self.solve()
        self.digger()
        return self

    def __findNthEmpty(self,board,n):
        _index = 1
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    if _index == n:
                        return (row,col)
                _index+=1
        return (-1,-1)

    
    def __solveForCreation(self,row,col):
        for n in range(1,10):
            if self.board[row][col]:
                if self.solve():
                    return self.board
                self.board[row][col] = 0
        return False

    def findNumberOfSolutions(self):
        _index = 0
        _listOfSolutions = []
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    _index += 1
        
        for i in range(1,_index+1):
            _boardCopy = copy.deepcopy(self)

            _row, _col = self.__findNthEmpty(_boardCopy.board,i)
            _boardCopySolution = _boardCopy.__solveForCreation(_row,_col)

            _listOfSolutions.append(self.boardToboard_string(input_board=_boardCopySolution))

        return list(set(_listOfSolutions))

    def digger(self, spacesLeft = 81):
        key = copy.deepcopy(self)
        _numToRemove = 46
        if spacesLeft < _numToRemove:
            _numToRemove = spacesLeft
        

        for i in range (0,3):
            _counter = 0
            while _counter < 4:
                _rRow = random.randint((3 * i), 2 + (3 * i))
                _rCol = random.randint((3 * i), 2 + (3 * i))
                if self.board[_rRow][_rCol] != 0:
                    self.board[_rRow][_rCol] = 0
                    _counter += 1
        _numToRemove -= 12
        _counter = 0
        while _counter < _numToRemove:
            _row = random.randint(0,8)
            _col = random.randint(0,8)

            if self.board[_row][_col] != 0:
                n = self.board[_row][_col]
                self.board[_row][_col] = 0

                if len(self.findNumberOfSolutions()) != 1:
                    self.board[_row][_col] = n
                    continue
            _counter += 1
        
        return self.board, key

    #TODO: Make a mehtod that adds user inputted tiles to the board. 
    
