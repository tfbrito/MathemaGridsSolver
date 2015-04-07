# -*- coding: UTF-8 -*-

import sys
from collections import Counter
from pyparsing import Word, Literal, nums, Forward, ParseException

import parser
sys.path
 
from z3 import *

import copy
 
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
 
print "\n Solving MathemaGrids \n"
 
if len(sys.argv) < 2:
    print "Missing input file"
    print "example: solveMathemaGrids.py <input file>"
    sys.exit()
 
filename = sys.argv[1]
 
f = open(filename, "r")
 
line = f.readline()
i = 0
table = []
while (line != ""):
    try:
        if (i % 2 == 0):  # it's an oddLine
            table = table + [oddLine.parseString(line)]
        else:  # it's an evenLine
            table = table + [evenLine.parseString(line)]
        i = i + 1
    except ParseException:
        try:  # it's the n-1 line
            table = table + [finalLine.parseString(line)]
            try:  # it's the last line
                line = f.readline()
                table = table + [lastLine.parseString(line)]
            except ParseException:
                print "erro na ?ltima linha!"
        except ParseException:
            print "erro na penultima linha!"
    line = f.readline()
 
print "==================\nINPUT\n=================="
 
for i in range(len(table)):
    print table[i]
 
print "==================\nFIM INPUT\n=================="
 
x_membros = (len(table[0]) - 1) / 2
y_membros = (len(table) - 1) / 2

X = [[Int("x_%s_%s" % (i + 1, j + 1)) for i in range(x_membros)]for j in range(y_membros)]

#Regras

# s� podem ser n�mero de 1 a 9
de_1_a_9  = [ And(1 <= X[j][i], X[j][i] <= x_membros*y_membros) for i in range(x_membros) for j in range(y_membros) ]

div_mult_por_1 = []
for i in range(len(table)):
    for j in range(len(table[i])):
        if (table[i][j]=='/' or table[i][j]=='*' ):
            if (i%2==0):
                div_mult_por_1.append(Not(X[i/2][(j+1)/2] == 1))
            else:
                div_mult_por_1.append(Not(X[(i+1)/2][j/2] ==1))


x=0
y=0
table2=[]

for i in range(len(table)):
    table2.append([])
    for j in range(len(table[i])):
        table2[i].append(table[i][j])

for i in range(0,len(table2)-1,2):
    for j in range(0,len(table2[i])-1,2):
        table2[i][j]=X[x][y]
        y+=1
    x+=1
    y=0

<<<<<<< HEAD
print "Imprissao das equacoes horizontais"	
=======
>>>>>>> 1a11ff264fe8a6a9e9ec0d7271c322e4cd1c1145
equacoes_horizontais=[]
equacao_aux=""
for i in range(0,len(table2)-1,2):
    for j in range(len(table2[i])):
        if(j!=0 and j%3==0 and j!=len(table2[i])-1):
            equacao_aux="("+equacao_aux+")"+str(table2[i][j])
        else:
            if(table2[i][j]=='.'):
                equacao_aux += "X["+str(i/2)+"]["+str(j/2)+"]"
            else:
                equacao_aux += str(table2[i][j])
    equacao_aux=equacao_aux.replace("=", "==")
    equacoes_horizontais.append(eval(equacao_aux))
    equacao_aux=""

<<<<<<< HEAD
print "Imprissao das equacoes verticais"
=======

>>>>>>> 1a11ff264fe8a6a9e9ec0d7271c322e4cd1c1145
equacoes_verticais=[]
equacao_aux=""
for i in range(0,len(table2)-2,2):
    for j in range(len(table2[i])):
        if(j!=0 and j%3==0 and j!=len(table2[i])-1):
            equacao_aux="("+equacao_aux+")"+str(table2[j][i])
        else:
            if(table2[j][i]=='.'):
                equacao_aux += "X["+str(j/2)+"]["+str(i/2)+"]"
            else:
                equacao_aux += str(table2[j][i])
    equacao_aux=equacao_aux.replace("=", "==")
    equacoes_verticais.append(eval(equacao_aux))
    equacao_aux=""

#Cada n�mero � unico na matriz
num_unico = [ Distinct([X[j][i] for i in range(x_membros)  for j in range(y_membros)]) ]

#como se faz a instancia ??? ver exemplo do A
instancia = [ If(table[i*2][j*2] is '.',
                  True,
                  X[i][j] == table[i*2][j*2])
               for i in range(x_membros) for j in range(y_membros) ]

solveMathemaGrid=de_1_a_9+num_unico+div_mult_por_1+equacoes_horizontais+equacoes_verticais

<<<<<<< HEAD
#como se faz a instancia ??? ver exemplo do A 
instancia = [ If(table[i][j] == "."),
                  True,
                  X[i][j] == table[i][j])
               for i in range(x_membros) for j in range(y_membros)]
			   
s=Solver()
print "ate aqui tudo bem "

s.add(solveMathemaGrid)
=======
s = Solver()

s.add(solveMathemaGrid+instancia)

print "\nConstraints\n"
for i in de_1_a_9:
    print i

for i in num_unico:
    print i

for i in div_mult_por_1:
    print i

for i in equacoes_horizontais:
    print i

for i in equacoes_verticais:
    print i
>>>>>>> 1a11ff264fe8a6a9e9ec0d7271c322e4cd1c1145

print "\nSolucao:\n"
if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(x_membros) ]
          for i in range(y_membros) ]
    for l in r:
        print l
else:
    print "\nimpossivel resolver\n"
