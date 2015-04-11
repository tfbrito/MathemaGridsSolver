# -*- coding: UTF-8 -*-

import sys
import kivy
import urllib2
import json
import pprint
import functools
import parser
import copy
kivy.require('1.7.1')
sys.path

from collections import Counter
from pyparsing import Word, Literal, nums, Forward, ParseException
from random import randrange
from z3 import *

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import  ListProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from functools import partial
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput

Builder.load_string('''
# define how clabel looks and behaves
<CLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos

<HeaderLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos
'''
)

counter = 0

class CLabel(ToggleButton):
    bgcolor = ListProperty([1,1,1])

class HeaderLabel(Label):
    bgcolor = ListProperty([0.108,0.476,0.611])

def calculate_col_size(num_cols):
    size = 0.1
    for i in range(num_cols-7):
        size = size - 0.001
    return size

class DataGrid(GridLayout):
    childs = []
    obj = 0
    obj_text = "null"
    all_sel = False
    count = 0
    solution = []
    def add_row(self, row_data, cols_size, instance, **kwargs):
        global counter
        self.rows += 1
        ##########################################################
        def change_on_press(self):
            childs = self.parent.children
            for ch in childs:
                if ch.id == self.id:
                    print ch.id
                    row_n = 0
                    if len(ch.id) == 11:
                        row_n = ch.id[4:5]
                    else:
                        row_n = ch.id[4:6]
                    for c in childs:
                        if (ch.id) == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:   
                                DataGrid.obj_text = c.text
                                c.state="normal"
                                c.text = '?' 
                                DataGrid.obj = c
                                Window.bind(on_key_down=DataGrid._on_keyboard_down)
                        else:
                            c.state="normal"

        def change_on_release(self):
            if self.state == "normal":
                self.state = "down"
                self.text = DataGrid.obj_text
            else:
                self.state = "normal"
                self.text = DataGrid.obj_text
        ##########################################################
        n = 0
        for item in row_data:
            if(item == ','):
                cell = CLabel(text=('[color=000000]' + item + '[/color]'), 
                                        background_normal="background_black.png",
                                        background_down="background_black.png",
                                        halign="center",
                                        markup=True,
                                        text_size=(0, None),
                                        size_hint_x=cols_size, 
                                        size_hint_y=None,
                                        height=40,
                                        id=("row_" + str(counter) + "_col_" + str(n)))
            elif(item == '.'):
                cell = CLabel(text=('[color=000000][/color]'), 
                                        background_normal="background_blue.png",
                                        background_down="background_pressed.png",
                                        halign="center",
                                        markup=True,
                                        on_press=partial(change_on_press),
                                        on_release=partial(change_on_release),
                                        text_size=(0, None),
                                        size_hint_x=cols_size, 
                                        size_hint_y=None,
                                        height=40,
                                        id=("x_" + str(counter) + "_" + str(n)))
            else:
                cell = CLabel(text=('[color=000000]' + item + '[/color]'), 
                                        background_normal="background_normal.png",
                                        background_down="background_normal.png",
                                        halign="center",
                                        markup=True,
                                        text_size=(0, None),
                                        size_hint_x=cols_size, 
                                        size_hint_y=None,
                                        height=40,
                                        id=("row_" + str(counter) + "_col_" + str(n)))
            cell_width = Window.size[0] * cell.size_hint_x
            cell.text_size=(cell_width - 30, None)
            cell.texture_update()
            self.add_widget(cell)
            n+=1
        counter += 1
        
    def select_all(self, instance, **kwargs):
        childs = self.parent.children
        DataGrid.childs = childs
        for ch in childs:
            for c in ch.children:
                c.state = "down"
        DataGrid.all_sel = True
        
        Window.bind(on_key_down=DataGrid._on_keyboard_down)

    def unselect_all(self, instance, **kwargs):
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = "normal"
        DataGrid.all_sel = False
        Window.unbind(on_key_down=DataGrid._on_keyboard_down)

    def hint(self,instance, **kwargs):
        childs = self.parent.children

        
        def check(childs,random_index_x,random_index_y,my_id):
            done = False
            sol = str(DataGrid.solution[random_index_x][random_index_y])
            for ch in childs:
                for c in ch.children:
                    if(str(c.id) == my_id):
                        
                        if(c.text[14:-8] != sol):
                            c.state = "normal" 
                            c.text = '[color=000000]' + sol + '[/color]'
                            DataGrid.solution[random_index_x][random_index_y] = "OK"
                            return True
            return False

        gotit = False
        gotit2 = False
        while(gotit == False):
            if(DataGrid.count >= x_membros * y_membros):
                gotit = True
                gotit2 = True
            else:
                while(gotit2 == False):
                    random_index_x = randrange(0,len(DataGrid.solution))
                    random_index_y = randrange(0,len(DataGrid.solution[random_index_x]))
                    if(str(DataGrid.solution[random_index_x][random_index_y]) != "OK"):
                        gotit2 = True
                        gotit = True

                my_id = "x_" + str(random_index_x*2) + "_" + str(random_index_y*2)
                if(check(childs,random_index_x,random_index_y,my_id) == True):
                    gotit = True
                    DataGrid.count = DataGrid.count + 1
        

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
            Window.unbind(on_key_down=DataGrid._on_keyboard_down)
            if(DataGrid.all_sel == True):
                if(keycode == 76): # Deleted pressed!
                    for ch in DataGrid.childs:
                        for c in ch.children:
                            if(c.id[:1] == 'x'):
                                c.state = "normal"
                                c.text = '[color=000000][/color]'
                DataGrid.all_sel = False
                DataGrid.solution = [row[:] for row in raw_solution]
                DataGrid.count = 0
            elif(text and DataGrid.obj.state == "down"):
                if (text.isdigit()):         
                    loc = list(DataGrid.obj.id[2:])
                    x = int(loc[0])/2
                    y = int(loc[2])/2
                    if(raw_solution[x][y].as_string() == text):
                        DataGrid.obj.state = "normal"
                        DataGrid.obj.text = '[color=000000]' + text + '[/color]'
                        DataGrid.solution[x][y] = "OK"
                    else:
                        DataGrid.obj.state = "normal"
                        DataGrid.obj.text = '[color=FF0000]' + text + '[/color]'

            elif(keycode == 76 and DataGrid.obj.state == "down"): # Deleted pressed!
                DataGrid.obj.state = "normal"
                DataGrid.obj.text = '[color=000000][/color]'

            return True
    
    def __init__(self, body_data, **kwargs):
        super(DataGrid, self).__init__(**kwargs)
        self.size_hint_y=None
        self.bind(minimum_height=self.setter('height'))
        self.cols = len(body_data[1])
        self.rows = len(body_data)
        self.spacing = [1,1]

        for row in range(len(body_data)):
            self.add_row(body_data[row], calculate_col_size(len(body_data)),self)



#############################################

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
raw_table = []

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
                print "Error on last line"
        except ParseException:
            print "Error on n-1 line"
    line = f.readline()

#Copy the table to initialize the puzzle and add the simbols
#for black spaces
raw_table = [row[:] for row in table]
for i in range(len(raw_table)):
    if(i%2!=0):
        raw_table[i].append(',')
        raw_table[i].append(',')

print "========\nINPUT\n========"

for i in range(len(table)):
    print table[i]
 
print "========\nFIM INPUT\n========"
 
x_membros = (len(table[0]) - 1) / 2
y_membros = (len(table) - 1) / 2

X = [[Int("x_%s_%s" % (i + 1, j + 1)) for i in range(x_membros)]for j in range(y_membros)]

#Rules

#Can only be numbers from 1 to 9
de_1_a_9  = [ And(1 <= X[j][i], X[j][i] <= x_membros*y_membros) for i in range(x_membros) for j in range(y_membros) ]

#Cannot be x1 or /1(but can be 1x)
div_mult_por_1 = []
for i in range(len(table)):
    for j in range(len(table[i])):
        if (table[i][j]=='/' or table[i][j]=='*' ):
            if (i%2==0):
                div_mult_por_1.append(Not(X[i/2][(j+1)/2] == 1))
            else:
                div_mult_por_1.append(Not(X[(i+1)/2][j/2] ==1))

# All operations must be equal or greater than 0
bigger_than_zero = []
for i in range(len(table)):
    for j in range(len(table[i])):
        if (i%2==0):
            if(table[i][j]=='-'):
                bigger_than_zero.append(Not(X[i/2][((j+1)/2)-1] - X[i/2][(j+1)/2] < 0))
                bigger_than_zero.append(Not(X[((i+1)/2-1)][j/2] - X[((i+1)/2)][(j+1)/2] < 0))

print "\n========Rule: Bigger than zero========\n"
for i in range(len(bigger_than_zero)):
    print bigger_than_zero[i]
print "\n========End Rule========\n"

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

# horizontal equations
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

# vertical equations
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

#Each number on matrix is unique
num_unico = [ Distinct([X[j][i] for i in range(x_membros)  for j in range(y_membros)]) ]

#Instance of the puzzle
instancia = [ If(table[i*2][j*2] is '.',
                  True,
                  X[i][j] == table[i*2][j*2])
               for i in range(x_membros) for j in range(y_membros) ]

#all together
solveMathemaGrid=de_1_a_9+num_unico+div_mult_por_1+equacoes_horizontais+equacoes_verticais+bigger_than_zero

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

print "\nSolution:\n"

if s.check() == sat:
    m = s.model()
    raw_solution = [ [ m.evaluate(X[i][j]) for j in range(x_membros) ]
          for i in range(y_membros) ]
    for l in raw_solution:
        print l
    DataGrid.solution = [row[:] for row in raw_solution]
else:
    print "\nImpossible!\n"

#Declaration of the grid object
grid = DataGrid(raw_table)
grid.rows = len(raw_table)

scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
scroll.add_widget(grid)
scroll.do_scroll_y = True
scroll.do_scroll_x = False

select_all_btn = Button(text="Sellect All", on_press=partial(grid.select_all))
unselect_all_btn = Button(text="Unsellect All", on_press=partial(grid.unselect_all))
hint_btn = Button(text="Hint", on_press=partial(grid.hint))


btn_grid = BoxLayout(orientation="vertical")
btn_grid.add_widget(select_all_btn)
btn_grid.add_widget(unselect_all_btn)
btn_grid.add_widget(hint_btn)

root = BoxLayout(orientation="horizontal")

root.add_widget(scroll)
root.add_widget(btn_grid)


class MathemaGridsApp(App):
    def build(self):
        return root

if __name__=='__main__':
    MathemaGridsApp().run()