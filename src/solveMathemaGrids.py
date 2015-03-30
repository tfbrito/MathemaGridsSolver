# -*- coding: UTF-8 -*-

import sys
sys.path

from z3 import *
from pyparsing import *

integer = Word( nums ) # simple unsigned integer
arithOp = Word( "+-*/", max=1 ) # arithmetic operators
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

print "\n Solving MathemaGrids \n"

if len(sys.argv)<2:
    print "Missing input file"
    print "example: solveMathemaGrids.py <input file>"
    sys.exit()

filename = sys.argv[1]

f = open(filename,"r") 

line=f.readline()
i=0
table=[]
while(line!=""):
	try:
		if(i%2==0): #it's an oddLine
			table = table + [oddLine.parseString(line)]
		else: #it's an evenLine
			table = table + [evenLine.parseString(line)]
		i=i+1
	except ParseException:
		try: #it's the n-1 line
			table = table + [finalLine.parseString(line)]
			try: #it's the last line
				line = f.readline()
				table = table + [lastLine.parseString(line)]
			except ParseException:
				print "erro na última linha!"
		except ParseException:
			print "erro na penultima linha!"
	line = f.readline()

print "==================\nINPUT\n=================="

for i in range(len(table)):
	print table[i]

print "==================\nFIM INPUT\n=================="