import random

class Board:
    def __init__(self,board_string=None):
        #creates a new, empty board
        self.__resetBoard()
        #if not null it will fill in the board with what was passed in
        if board_string:
            self.board_string = board_string
            for row in range(9):
                for col in range(9):
                    self.board[row][col] = int(board_string[0])
                    board_string = board_string[1:]
        # if null then leave the board empty
        else:
            self.board_string = None

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
            self.board_string = ''.join([str(i) for j in input_board for i in j])
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
        boxC = space[0] // 3
        #make sure num is not in the same 3x3 'box'
        for i in range(3):
            for j in range(3):
                if self.board[i + (boxR * 3)][j + (boxC * 3)] == num:
                    return False

        #if you've made it here, its a valid guess so far!
        return True

    def solve(self):
        pass
    
