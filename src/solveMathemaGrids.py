# -*- coding: UTF-8 -*-

from z3 import Int, And, Not


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


def calculate_col_size(num_cols):
    size = 0.1
    for i in range(num_cols-7):
        size -= 0.001
    return size

