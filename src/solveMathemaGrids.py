# -*- coding: UTF-8 -*-
import parsing
import generate_board

from functools import partial
from random import randrange
from z3 import Int, And, Not, Distinct, If, Solver, sat

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
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

Builder.load_string('''
<CLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos
'''
)

def complete_board(board):
    for i in range(len(board)):
        if(i%2!=0):
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
    obj_text = None
    all_sel = False
    count = 0
    solution = []
    raw_table = []
    validate = False
    hints = False
    hints_all = False
    def add_row(self, row_data, cols_size, instance, **kwargs):
        global counter
        self.rows += 1

        def change_on_press(self):
            childs = self.parent.children
            for ch in childs:
                if ch.id == self.id:
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
        info_lbl.text = '[color=008000]All selected[/color]'
        childs = self.parent.children
        DataGrid.childs = childs
        for ch in childs:
            for c in ch.children:
                c.state = "down"
        DataGrid.all_sel = True
        Window.bind(on_key_down=DataGrid._on_keyboard_down)

    def unselect_all(self, instance, **kwargs):
        info_lbl.text = 'MathemaGrids puzzle'
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = "normal"
        DataGrid.all_sel = False
        Window.unbind(on_key_down=DataGrid._on_keyboard_down)

    def hint(self,instance, **kwargs):
        if(DataGrid.hints):
            childs = self.parent.children

            def check(childs,random_index_x,random_index_y,my_id):
                done = False
                sol = str(DataGrid.solution[random_index_x][random_index_y])
                for ch in childs:
                    for c in ch.children:
                        if(str(c.id) == my_id and DataGrid.hints_all != True):
                            if(c.text[14:-8] != sol):
                                c.state = "normal" 
                                c.text = '[color=000000]' + sol + '[/color]'
                                DataGrid.solution[random_index_x][random_index_y] = "OK"
                                return True
                        elif(str(c.id) == my_id and DataGrid.hints_all == True):
                            if(c.text == '[color=000000][/color]' or c.text == '[color=FF0000][/color]'):
                                c.state = "normal" 
                                c.text = '[color=000000]' + sol + '[/color]'
                                DataGrid.solution[random_index_x][random_index_y] = "OK"
                                return True
                            else: 
                                return -1
                return False

            gotit = False
            gotit2 = False
            while(gotit == False):
                if(DataGrid.count >= len(DataGrid.solution) * len(DataGrid.solution[0])):
                    info_lbl.text = '[color=008000]No more hints![/color]'
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
                    res = check(childs,random_index_x,random_index_y,my_id)
                    if(res == True):
                        gotit = True
                        DataGrid.count = DataGrid.count + 1
                    elif(res == -1):
                        gotit2 = False
                        gotit = False
        else:
            info_lbl.text = '[color=FF0000]Hints are disabled!\nEnable them on the settings panel.[/color]'
            
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
            info_lbl.text = 'MathemaGrids puzzle'
            Window.unbind(on_key_down=DataGrid._on_keyboard_down)
            if(DataGrid.all_sel == True):
                if(keycode == 76): # Deleted pressed!
                    for ch in DataGrid.childs:
                        for c in ch.children:
                            if(c.id[:1] == 'x'):
                                c.state = "normal"
                                c.text = '[color=000000][/color]'
                DataGrid.all_sel = False
                DataGrid.solution = [row[:] for row in DataGrid.raw_table]
                DataGrid.count = 0
            elif(text and DataGrid.obj.state == "down"):
                if (text.isdigit()):         
                    loc = list(DataGrid.obj.id[2:])
                    x = int(loc[0])/2
                    y = int(loc[2])/2
                    if(DataGrid.validate == True):
                        if(DataGrid.raw_table[x][y].as_string() == text):
                            DataGrid.obj.state = "normal"
                            DataGrid.obj.text = '[color=000000]' + text + '[/color]'
                            DataGrid.solution[x][y] = "OK"
                        else:
                            DataGrid.obj.state = "normal"
                            DataGrid.obj.text = '[color=FF0000]' + text + '[/color]'
                    else:
                        DataGrid.obj.state = "normal"
                        DataGrid.obj.text = '[color=000000]' + text + '[/color]'

            elif(keycode == 76 and DataGrid.obj.state == "down"): # Deleted pressed!
                DataGrid.obj.state = "normal"
                DataGrid.obj.text = '[color=000000][/color]'

            return True

    def reset_board(self):
        childs = self.parent.children
        for ch in childs:
            for c in reversed(ch.children):
                self.remove_widget(c)

    def generate(self, instance, **kwargs):
        global counter
        counter = 0
        DataGrid.childs = []
        DataGrid.obj = 0
        DataGrid.obj_text = None
        DataGrid.all_sel = False
        DataGrid.count = 0
        DataGrid.reset_board(self)
        res = generate_board.generate(3,0)

        complete_board(res[0])
        self.cols = len(res[0][1])
        self.rows = len(res[0])
        self.spacing = [1,1] 
        for row in range(len(res[0])):
            self.add_row(res[0][row], calculate_col_size(len(res[0])),self)
        DataGrid.solution = res[1]
        DataGrid.raw_table = [row[:] for row in res[1]]
    
    def __init__(self, body_data, **kwargs):
        super(DataGrid, self).__init__(**kwargs)
        self.size_hint_y=None
        self.bind(minimum_height=self.setter('height'))
        if(body_data):
            self.cols = len(body_data[1])
            self.rows = len(body_data)
            self.spacing = [1,1]

            for row in range(len(body_data)):
                self.add_row(body_data[row], calculate_col_size(len(body_data)),self)

###
checkbox1 = DataGrid.validate
checkbox2 = DataGrid.hints
checkbox3 = DataGrid.hints_all
def settings_panel(self):
    info_lbl.text = 'MathemaGrids puzzle'
    global checkbox1
    global checkbox2
    global checkbox3

    def on_checkbox_active(checkbox, value):        
        if(checkbox.id == "ck_validate"):
            global checkbox1
            checkbox1 = value
        elif(checkbox.id == "ck_hints"):
            global checkbox2
            checkbox2 = value
        elif(checkbox.id == "ck_hints_all"):
            global checkbox3
            checkbox3 = value        

    def save_settings(self):
        DataGrid.validate = checkbox1
        DataGrid.hints = checkbox2
        DataGrid.hints_all = checkbox3

    label1 = Label(text='Validar jogadas ao introduzir', id="lbl_validate")
    label2 = Label(text='Activar hints', id="lbl_hints")
    label3 = Label(text='Hints preenchem apenas campos vazios', id="lbl_hints_all")
    check1 = CheckBox(id="ck_validate",active=DataGrid.validate)
    check2 = CheckBox(id="ck_hints",active=DataGrid.hints)
    check3 = CheckBox(id="ck_hints_all",active=DataGrid.hints_all)
    check1.bind(active=on_checkbox_active)
    check2.bind(active=on_checkbox_active)
    check3.bind(active=on_checkbox_active)

    settings_grid = GridLayout(cols=2)
    settings_grid.add_widget(label1)
    settings_grid.add_widget(check1)
    settings_grid.add_widget(label2)
    settings_grid.add_widget(check2)
    settings_grid.add_widget(label3)
    settings_grid.add_widget(check3)
    
    view = ModalView(auto_dismiss=False)
    
    cancel_btn = Button(text='Cancel')
    save_btn = Button(text="Save", on_press=save_settings) 
    cancel_btn.bind(on_press=view.dismiss)
    save_btn.bind(on_release=view.dismiss)

    modal_layout = BoxLayout(orientation="vertical")
    modal_layout.add_widget(settings_grid)
    modal_layout.add_widget(save_btn)
    modal_layout.add_widget(cancel_btn)

    view.add_widget(modal_layout)
    view.open()

############################
board = generate_board.generate(2,0)
complete_board(board[0])

#Declaration of the grid object
grid = DataGrid(board[0])
grid.rows = len(board[0])

DataGrid.solution = board[1]
DataGrid.raw_table = [row[:] for row in board[1]]

scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
scroll.add_widget(grid)
scroll.do_scroll_y = True
scroll.do_scroll_x = False

generate_btn = Button(text="Generate puzzle", on_press=partial(grid.generate))
select_all_btn = Button(text="Sellect All", on_press=partial(grid.select_all))
unselect_all_btn = Button(text="Unsellect All", on_press=partial(grid.unselect_all))
hint_btn = Button(text="Hint", on_press=partial(grid.hint))
settings_btn = Button(text="Settings", on_press=settings_panel)

info_lbl = Label(text='MathemaGrids puzzle', id="lbl_info", markup=True)

btn_grid = BoxLayout(orientation="vertical")
btn_grid.add_widget(generate_btn)
btn_grid.add_widget(select_all_btn)
btn_grid.add_widget(unselect_all_btn)
btn_grid.add_widget(hint_btn)
btn_grid.add_widget(settings_btn)
btn_grid.add_widget(info_lbl)

root = BoxLayout(orientation="horizontal")

root.add_widget(scroll)
root.add_widget(btn_grid)

class MathemaGridsApp(App):
    def build(self):
        return root

if __name__=='__main__':
    MathemaGridsApp().run()