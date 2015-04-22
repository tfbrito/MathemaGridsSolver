# -*- coding: UTF-8 -*-
import sys

filename = None

def solve():
	print filename
	print "Let's solve the puzzle!"

def generate():
    print "Generate a puzzle"

def play():
   	print "Let's play a game!"

def exit():
	print "Exiting...."
	sys.exit(1)

options = {1 : solve,
           2 : generate,
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