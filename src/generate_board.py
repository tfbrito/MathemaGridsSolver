from z3 import Int, And, Not, Distinct, Solver, sat

import random


def generate_symbols(size):
    board = []
    symbols = ['+', '-', '*', '/']

    for i in range(size*2-1):
        board.append([])
        if i % 2 == 0:
            for j in range(size*2-1):
                if j % 2 == 0:
                    board[i].append('.')
                else:
                    l = random.choice(symbols)
                    board[i].append(l)
        else:
            for j in range(size*2-1):
                if j % 2 == 0:
                    l = random.choice(symbols)
                    board[i].append(l)
                else:
                    board[i].append(',')
    return board


def attempt_to_solve(board):

    size = len(board[0])/2 + 1

    x = [[Int("x_%s_%s" % (i + 1, j + 1)) for i in range(size)]for j in range(size)]

    max_range = [And(1 <= x[j][i], x[j][i] <= size*size) for i in range(size) for j in range(size)]

    not_one_exceptions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '/' or board[i][j] == '*':
                if i % 2 == 0:
                    not_one_exceptions.append(Not(x[i/2][(j+1)/2] == 1))
                else:
                    not_one_exceptions.append(Not(x[(i+1)/2][j/2] == 1))

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
                            if n > 2 and not(board[i][n] == "."):
                                equation = "("+equation+")"+str(board[i][n])
                            else:
                                if board[i][n] == ".":
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
                            if n > 2 and not(board[n][j] == "."):
                                equation = "("+equation+")"+str(board[n][j])
                            else:
                                if board[n][j] == ".":
                                    equation += "x["+str(n/2)+"]["+str(j/2)+"]"
                                else:
                                    equation += board[n][j]
                        equation = equation + "-" + "x[" + str((i+1)/2) + "][" + str(j/2)+"]" + ">0"
                        bigger_than_zero.append(eval(equation))

    multiple = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if i % 2 == 0:
                if board[i][j] == '/':
                    multiple.append(x[i/2][(j-1)/2] % x[i/2][(j+1)/2] == 0)
            else:
                if board[i][j] == '/':
                    multiple.append(x[(i-1)/2][j/2] % x[(i+1)/2][j/2] == 0)

    unique = [Distinct([x[j][i] for i in range(size) for j in range(size)])]

    rules = unique+bigger_than_zero+not_one_exceptions+max_range+multiple

    s = Solver()
    s.add(rules)
    s.set("soft_timeout", 100)
    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(x[i][j]) for j in range(size)] for i in range(size)]
        return r
    else:
        return 0


def generate_results(board, solution):
    for i in range(0, len(board), 2):
        equation = ""
        for j in range(len(board[i])):
            if j > 2 and not(board[i][j] == "."):
                equation = "("+equation+")"+str(board[i][j])
            else:
                if board[i][j] == ".":
                    equation += str(solution[i/2][j/2])
                else:
                    equation += str(board[i][j])

        result = eval(equation)
        board[i].append('=')
        board[i].append(str(result))

    board.append([])
    board.append([])
    for i in range(0, len(board)-2, 2):
        equation = ""
        for j in range(len(board[i])-2):
            if j > 2 and not(board[j][i] == "."):
                equation = "("+equation+")"+str(board[j][i])
            else:
                if board[j][i] == ".":
                    equation += str(solution[j/2][i/2])
                else:
                    equation += str(board[j][i])

        result = eval(equation)
        board[j+1].append('=')
        board[j+2].append(str(result))
        if i < len(board)-3:
            board[j+1].append(",")
            board[j+2].append(",")

    return board


def generate(size, hints):
    generated_board = generate_symbols(size)
    solution = attempt_to_solve(generated_board)
    while solution == 0:
        generated_board = generate_symbols(size)
        solution = attempt_to_solve(generated_board)

    generated_board_with_results = generate_results(generated_board, solution)
    horizontal_indices = [ind for ind in range(size)]
    vertical_indices = [ind for ind in range(size)]

    while hints > 0:
        horizontal_index = random.choice(horizontal_indices)
        vertical_index = random.choice(vertical_indices)
        horizontal_indices.remove(horizontal_index)
        vertical_indices.remove(vertical_index)
        generated_board_with_results[horizontal_index*2][vertical_index*2] = str(solution[horizontal_index][vertical_index])
        hints -= 1

    return generated_board_with_results, solution

