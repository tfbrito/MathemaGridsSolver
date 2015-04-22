# -*- coding: UTF-8 -*-
import sys
import parsing
import time

from solveMathemaGrids import complete_board, solve
from generate_board import generate

filename = None

def solve_puzzle():
	print "\nLet's solve the puzzle!\n"
	input_puzzle = parsing.read_board(filename)
	
	print "\nThe Input puzzle:\n"
	for i in range(len(input_puzzle)):
		print input_puzzle[i]

	complete_board(input_puzzle)
	print "\nSolving the puzzle. Please wait..."
	solution = solve(input_puzzle)
	print "\nSolution:\n"
	for i in range(len(solution)):
		print solution[i]

	val = raw_input("\nDo you want to save this solution to file? (y/N): ")
	if(str(val) == "y" or str(val) == "Y"):
		val2 = raw_input("Which name do you want? ")
		print "\nSaving solution. Please wait...\n"
		parsing.save_board(solution,str(val2))
		print "File saved under name " + str(val2) + " in current directory"

	time.sleep(5)
	menu()


def generate_puzzle():
	print "\nLet's generate an new puzzle\n"
	print "2 - Puzzle of dimension 5x5"
	print "3 - Puzzle of dimension 7x7 (Original)"
	print "4 - Puzzle of dimension 9x9 (WARNING: It could take a long time!!!)"
	print "Another number bigger than 4 (WARNING: It could not end!!)"
	val = input("\nWich one do you want? ")
	if(val>2):
		val2 = input("\nDo you want a puzzle with hints? (0/1/2/3): ")
		if(val2 == 0 or val2 == 1 or val2 == 2 or val2 == 3):
			print "\nGenerating puzzle of size " + str(val) + " with " + str(val2) + " hints. Please Wait..."
			puzzle, solution = generate(val,val2)
		else:
			print "Invalid option. Considering 0 hints."
			print "\nGenerating puzzle of size " + str(val) + " with 0 hints. Please Wait..."
			puzzle, solution = generate(val,0)
	else:
		print "Wrong choice!"
		generate_puzzle()

	print "\nThe Generated puzzle:\n"
	for i in range(len(puzzle)):
		print puzzle[i]

	print "\nIt's Solution:\n"
	for i in range(len(solution)):
		print solution[i]

	val3 = raw_input("\nDo you want to save this puzzle and solution to file? (y/N): ")
	if(str(val3) == "y" or str(val3) == "Y"):
		val4 = raw_input("Which name do you want? ")
		print "\nSaving puzzle and solution. Please wait...\n"
		parsing.save_board(puzzle,"puzzle-"+str(val4))
		parsing.save_board(solution,"solution-"+str(val4))
		print "Files saved under names puzzle-" + str(val4) + " and solution-" + str(val4) + " in current directory"

	time.sleep(5)
	menu()

def play():
   	print "Let's play a game!"

def exit():
	print "Exiting...."
	sys.exit(1)

options = {1 : solve_puzzle,
           2 : generate_puzzle,
           3 : play,
           9 : exit,
}

def menu():
	flag = True
	print "-------------------------------------"
	print "Welcome to MathemaGrids Puzzle Solver"
	print "-------------------------------------"
	print "\n"
	print "----------------"
	print "|     Menu     |"
	print "----------------"
	print "1 - Solve Puzzle from file"
	print "2 - Generate puzzle"
	print "3 - Play puzzle"
	print "9 - Exit"
	while(flag):
		var = input("What is your choise? ")
		if(var in options):
			flag = False
			options[var]()
		else:
			print "Wrong choise, please try again!"

if(len(sys.argv)==1):
	import gameGui
	gameGui.MathemaGridsApp().run()
elif(sys.argv[1] == "--console"):
	if(len(sys.argv)>2):
		filename = sys.argv[2]
		menu()
	else:
		print "Missing input file!"