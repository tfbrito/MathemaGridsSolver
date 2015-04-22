# MathemaGridsSolver
Use of Z3 smt solver with Python api to solve the MathemasGrid puzzle 

## Dependencies
sudo apt-get install g++

Z3Solver: https://github.com/Z3Prover/z3

pyparsing: http://pyparsing.wikispaces.com/

#####Kivy:
- sudo add-apt-repository ppa:kivy-team/kivy
- sudo apt-get install python-kivy

##Usage
python src/game.py < flags > < file >

#####flags:
--console -> Executes in console mode

Notes: 
- By default the game initializes in GUI mode
- < flags > and < file > are optional and intended for console mode


