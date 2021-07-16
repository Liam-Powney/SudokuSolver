input = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

def printSudoku(sudoku):
    for i in range(len(sudoku)):
        print(str(sudoku[i]))
    print("\n")

# finds and returns the indices of the next empty box of the input sudoku; returns True if sudoku is full
def findNextEmpty(sudoku):
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            if sudoku[i][j] == 0:
                return [i, j]
    return False

# checks the value of a box in the input sudoku with inidces i, j and returns true if the value is valid, false if the value is not
def isValidNumber(sudoku, x, y):
    # check row
    for i in range(len(sudoku[x])):
        if ( sudoku[x][i] == sudoku[x][y] ) and ( i != y ):
            return False
    # check column
    for j in range(len(sudoku)):
        if ( sudoku[j][y] == sudoku[x][y] ) and ( j != x ):
            return False
    # check box
    for i in range( ( x // 3 ) * 3 , (( x // 3) * 3) + 3 ):
        for j in range(( y // 3 ) * 3 , (( y // 3) * 3) + 3):
            if ( sudoku[i][j] == sudoku[x][y] ) and ( ( i != x ) and ( j != y ) ):
                return False
    return True

# recursive backtracking sudoku solving algorithm: returns true if sudoku is solved, false if there is no solution
def bt_SudokuSolver(sudoku):
    # find the next empty box
    box = findNextEmpty(sudoku)
    # if no next empty box, return True ( i.e. sudoku is sovled )
    if box == False:
        return True
    # try all values from 1 to 9 in box
    for i in range(1, 10):
        sudoku[box[0]][box[1]] = i
        # if the value is valid, recursively call the solver function to act on the next empty box
        if isValidNumber(sudoku, box[0], box[1]) == True:
            if bt_SudokuSolver(sudoku):
                return True
    sudoku[box[0]][box[1]] = 0
    return False
