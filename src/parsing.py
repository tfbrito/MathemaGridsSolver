# -*- coding: UTF-8 -*-
import sys
sys.path

from pyparsing import Word, Literal, nums, Forward, ParseException

def read_board(file):
    integer = Word(nums)  # simple unsigned integer
    arithOp = Word("+-*/", max=1)  # arithmetic operators
    equal = Literal("=")

    identifier2 = integer | "." | ","
    oddLine = Forward()
    oddLine << ((identifier2 + arithOp + oddLine) | identifier2 + "=" + integer)

    evenLine = Forward()
    evenLine << ((arithOp + "," + evenLine) | arithOp)

    finalLine = Forward()
    finalLine << ((equal + "," + finalLine) | equal)

    lastLine = Forward()
    lastLine << ((integer + "," + lastLine) | integer)

    f = open(file, "r")
    line = f.readline()
    i = 0
    table = []
    while line != "":
        try:
            if i % 2 == 0:  # it's an oddLine
                table = table + [oddLine.parseString(line)]
            else:  # it's an evenLine
                table = table + [evenLine.parseString(line)]
            i += 1
        except ParseException:
            try:  # it's the n-1 line
                table = table + [finalLine.parseString(line)]
                try:  # it's the last line
                    line = f.readline()
                    table = table + [lastLine.parseString(line)]
                except ParseException:
                    print "Error on last line"
            except ParseException:
                print "Error on n-1 line"
        line = f.readline()
    return table

def save_board(board_to_save, text_file_name):
    name = text_file_name+'.txt'  # Name of text file coerced with +.txt

    try:
        board_file = open(name, 'w')   # Trying to create a new file or open one
    except:
        print('Something went wrong! Can\'t tell what?')
        sys.exit(0)  # quit Python

    for line in range(len(board_to_save)):
        for column in range(len(board_to_save[line])):
            if line % 2 == 0:
                board_file.write(str(board_to_save[line][column]))
            else:
                if column <= len(board_to_save[1]):
                    board_file.write(str(board_to_save[line][column]))
        board_file.write("\n")

    board_file.close()