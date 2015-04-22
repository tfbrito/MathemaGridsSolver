# -*- coding: UTF-8 -*-
from z3 import Int, And, Not, Distinct, If, Solver, sat


def complete_board(board):
    for i in range(len(board)):
        if i % 2 != 0:
            board[i].append(',')
            board[i].append(',')


def solve(board):
    size = (len(board[0]) - 1) / 2

    x = [[Int("x_%s_%s" % (i + 1, j + 1)) for i in range(size)] for j in range(size)]

    # Rules

    # Can only be numbers from 1 to 9
    max_size = [And(1 <= x[j][i], x[j][i] <= size * size) for i in range(size) for j in range(size)]

    # Cannot be x1 or /1(but can be 1x)
    not_one_exceptions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if str(board[i][j]) == "/" or str(board[i][j]) == "*":
                if i % 2 == 0:
                    not_one_exceptions.append(Not(x[i/2][(j+1)/2] == 1))
                else:
                    not_one_exceptions.append(Not(x[(i+1)/2][j/2] == 1))

    # All operations must be equal or greater than 0
    bigger_than_zero = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if i % 2 == 0:
                if board[i][j] == '-':
                    if j == 1:
                        bigger_than_zero.append(Not(x[i/2][(j-1)/2] - x[i/2][(j+1)/2] < 0))
                    else:
                        equation = ""
                        for n in range(j):
                            if n > 2 and str(board[i][n]) != "." and not(board[i][n].isdigit()):
                                equation = "("+equation+")"+str(board[i][n])
                            else:
                                if board[i][n] == "." or board[i][n].isdigit():
                                    equation += "x["+str(i/2)+"]["+str(n/2)+"]"
                                else:
                                    equation += board[i][n]
                        equation = equation + "-" + "x[" + str(i/2) + "][" + str((j+1)/2)+"]" + ">0"
                        bigger_than_zero.append(eval(equation))
            else:
                if board[i][j] == '-':
                    if i == 1:
                        bigger_than_zero.append(Not(x[(i-1)/2][j/2] - x[(i+1)/2][j/2] < 0))
                    else:
                        equation = ""
                        for n in range(i):
                            if n > 2 and board[n][j] != "." and not(board[n][j].isdigit()):
                                equation = "("+equation+")"+str(board[n][j])
                            else:
                                if board[n][j] == "." or board[n][j].isdigit():
                                    equation += "x["+str(n/2)+"]["+str(j/2)+"]"
                                else:
                                    equation += str(board[n][j])
                        equation = equation + "-" + "x[" + str((i+1)/2) + "][" + str(j/2)+"]" + ">0"
                        bigger_than_zero.append(eval(equation))

    x1 = 0
    y1 = 0
    board2 = []

    for i in range(len(board)):
        board2.append([])
        for j in range(len(board[i])):
            board2[i].append(board[i][j])

    for i in range(0, len(board2) - 1, 2):
        for j in range(0, len(board2[i]) - 1, 2):
            board2[i][j] = x[x1][y1]
            y1 += 1
        x1 += 1
        y1 = 0

    # horizontal equations
    horizontal_equations=[]
    equation = ""
    for i in range(0, len(board2)-1, 2):
        for j in range(len(board2[i])):
            if j > 2 and board[i][j] != "." and not(board[i][j].isdigit()) and j != len(board2[i])-1:
                equation = "("+equation+")"+str(board2[i][j])
            else:
                if board2[i][j] == '.':
                    equation += "x["+str(i/2)+"]["+str(j/2)+"]"
                else:
                    equation += str(board2[i][j])
        equation = equation.replace("=", "==")
        horizontal_equations.append(eval(equation))
        equation = ""

    # vertical equations
    vertical_equations = []
    equation = ""
    for i in range(0,len(board2)-2,2):
        for j in range(len(board2[i])):
            if j > 2 and board[i][j] != "." and not(board[i][j].isdigit()) and j != len(board2[i])-1:
                equation = "("+equation+")"+str(board2[j][i])
            else:
                if board2[j][i] == '.':
                    equation += "x["+str(j/2)+"]["+str(i/2)+"]"
                else:
                    equation += str(board2[j][i])
        equation = equation.replace("=", "==")
        vertical_equations.append(eval(equation))
        equation = ""

    # Each number on matrix is unique
    unique = [Distinct([x[j][i] for i in range(size) for j in range(size)])]

    # Instance of the puzzle
    instance = [If(board[i*2][j*2] is ".",
                    True,
                    x[i][j] == board[i*2][j*2]) for i in range(size) for j in range(size)]

    # All together
    rules = instance+max_size + unique + not_one_exceptions + horizontal_equations + vertical_equations + bigger_than_zero + not_one_exceptions
    s = Solver()

    s.add(rules)

    if s.check() == sat:

        m = s.model()
        r = [[m.evaluate(x[i][j]) for j in range(size)]
             for i in range(size)]
        return r
    else:
        return []



def calculate_col_size(num_cols):
    size = 0.1
    for i in range(num_cols-7):
        size -= 0.001
    return size