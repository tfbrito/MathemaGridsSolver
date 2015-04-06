# -*- coding: UTF-8 -*-
<<<<<<< HEAD
 
import sys
from collections import Counter
from pyparsing import Word, Literal, nums, Forward, ParseException
 
sys.path
 
from z3 import *
 
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
 
print "Membros a preencher na horizontal:", x_membros
print "Membros a preencher na vertical:", y_membros
 
X = [[Int("x_%s_%s" % (i + 1, j + 1)) for i in range(x_membros)]for j in range(y_membros)]
 
for i in X:
    print i
#Regras

# só podem ser número de 1 a 9
de_1_a_9  = [ And(1 <= X[j][i], X[j][i] <= x_membros*y_membros) for i in range(x_membros) for j in range(y_membros) ]
 
 
print "Regras para os numeros serem escritos de 1 a 9"
for i in de_1_a_9:
    print i;
 
div_mult_por_1 = []
for i in range(len(table)):
    for j in range(len(table[i])):
        if (table[i][j]=='/' or table[i][j]=='*' ):
            if (i%2==0):
                div_mult_por_1.append(Not(X[i/2][(j+1)/2] == 1))
            else:
                div_mult_por_1.append(Not(X[(i+1)/2][j/2] ==1))
print "Regras para nao se poder dividir e multiplicar por 1"
for i in div_mult_por_1:
    print i;
 
 
x=0
y=0
print "imprimir as posicoes e os numeros:"
for i in range(0,len(table)-1,2):
    for j in range(0,len(table[i])-1,2):
        table[i][j]=X[x][y]
        y+=1
    x+=1
    y=0
 
for i in table:
    print i

print "Imprissao das equiacoes horizontais"	
equacoes_horizontais=[]
equacao_aux=""
for i in range(0,len(table)-1,2):
    for j in range(len(table[i])):
        if(j!=0 and j%3==0 and j!=len(table[i])-1):
            equacao_aux="("+equacao_aux+")"+str(table[i][j])
        else:
            equacao_aux+=str(table[i][j])
    print equacao_aux
    equacoes_horizontais.append(equacao_aux)
    equacao_aux=""

print "Imprissao das equiacoes verticais"	
equacoes_verticais=[]
equacao_aux=""
for i in range(0,len(table)-2,2):
    for j in range(len(table[i])):
        if(j!=0 and j%3==0 and j!=len(table[i])-1):
            equacao_aux="("+equacao_aux+")"+str(table[j][i])
        else:
            equacao_aux+=str(table[j][i])
    print equacao_aux
    equacoes_verticais.append(equacao_aux)
    equacao_aux=""

#Cada número é unico na matriz
num_unico = [ Distinct([X[j][i] for i in range(x_membros)  for j in range(y_membros)]) ]

print "numero unico"
for i in num_unico:
    print i;
	
solveMathemaGrid=de_1_a_9+num_unico+div_mult_por_1+equacoes_horizontais+equacoes_verticais
 
print "ate aqui tudo bem "

#como se faz a instancia ??? ver exemplo do A 
instancia = [ If(table[i][j] == 0, 
                  True, 
                  X[i][j] == table[i][j]) 
               for i in range(x_membros) for j in range(y_membros)]
			   
s=Solver()
print "ate aqui tudo bem "

s.add(solveMathemaGrid)
print "\nSolucao:\n"
if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(x_membros) ]
          for i in range(y_membros) ]
    for l in r:
        print l
