# -*- coding: UTF-8 -*-
import generate_board
import parsing
import re

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

from functools import partial
from random import randrange
from solveMathemaGrids import complete_board
from solveMathemaGrids import calculate_col_size

Builder.load_string('''
<CLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos
''')

counter = 0

class CLabel(ToggleButton):
    bgcolor = ListProperty([1, 1, 1])

class HeaderLabel(Label):
    bgcolor = ListProperty([0.108, 0.476, 0.611])

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
    board_size = "2"

    def load_from_filechooser(self, filechooser, path):
        global counter
        counter = 0
        DataGrid.childs = []
        DataGrid.obj = 0
        DataGrid.obj_text = None
        DataGrid.all_sel = False
        DataGrid.count = 0
        DataGrid.reset_board(self)
        res = parsing.read_board(filechooser.selection[0])

        complete_board(res)
        self.cols = len(res[1])
        self.rows = len(res)
        self.spacing = [1, 1]
        for row in range(len(res)):
            self.add_row(res[row], calculate_col_size(len(res)), self)

    def open(self, instance, **kwargs):
        view = ModalView(auto_dismiss=False)

        filechooser = ""
        chooser_grid = BoxLayout()
        fileChooser = FileChooserListView(id=filechooser, path="/home/")

        buttons = BoxLayout(height=30, size_hint_y=None)
        cancel_btn = Button(text='Cancel')
        open2_btn = Button(text="Open")

        cancel_btn.bind(on_press=view.dismiss)
        open2_btn.bind(on_release=partial(self.load_from_filechooser, fileChooser), on_press=view.dismiss)

        modal_layout = BoxLayout(orientation="vertical")
        modal_layout.add_widget(chooser_grid)
        modal_layout2 = BoxLayout(orientation="horizontal", size_hint_y=None)
        modal_layout2.add_widget(open2_btn)
        modal_layout2.add_widget(cancel_btn)

        modal_layout.add_widget(modal_layout2)
        chooser_grid.add_widget(fileChooser)

        view.add_widget(modal_layout)
        view.open()

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
                        if ch.id == c.id:
                            if c.state == "normal":
                                c.state = "down"
                            else:
                                DataGrid.obj_text = c.text
                                c.state = "normal"
                                c.text = '?'
                                DataGrid.obj = c
                                Window.bind(on_key_down=DataGrid._on_keyboard_down)
                        else:
                            c.state = "normal"

        def change_on_release(self):
            if self.state == "normal":
                self.state = "down"
                self.text = DataGrid.obj_text
            else:
                self.state = "normal"
                self.text = DataGrid.obj_text

        n = 0
        for item in row_data:
            if item == ',':
                cell = CLabel(text=('[color=000000]' + item + '[/color]'),
                                        background_normal="resources/background_black.png",
                                        background_down="resources/background_black.png",
                                        halign="center",
                                        markup=True,
                                        text_size=(0, None),
                                        size_hint_x=cols_size,
                                        size_hint_y=None,
                                        height=40,
                                        id=("row_" + str(counter) + "_col_" + str(n)))
            elif item == '.':
                cell = CLabel(text=('[color=000000][/color]'),
                                        background_normal="resources/background_blue.png",
                                        background_down="resources/background_pressed.png",
                                        halign="center",
                                        markup=True,
                                        on_press=partial(change_on_press),
                                        on_release=partial(change_on_release),
                                        text_size=(0, None),
                                        size_hint_x=cols_size,
                                        size_hint_y=None,
                                        height=40,
                                        id=("x_" + str(counter/2) + "_" + str(n/2)))
            else:
                cell = CLabel(text=('[color=000000]' + item + '[/color]'),
                                        background_normal="resources/background_normal.png",
                                        background_down="resources/background_normal.png",
                                        halign="center",
                                        markup=True,
                                        text_size=(0, None),
                                        size_hint_x=cols_size,
                                        size_hint_y=None,
                                        height=40,
                                        id=("row_" + str(counter) + "_col_" + str(n)))
            cell_width = Window.size[0] * cell.size_hint_x
            cell.text_size = (cell_width - 30, None)
            cell.texture_update()
            self.add_widget(cell)
            n += 1
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

    def validate(self, instance, **kwargs):
        DataGrid.childs = self.parent.children
        for ch in DataGrid.childs:
            for c in ch.children:
                if re.search("x_\d+_\d+", str(c.id)):
                    index_x, index_y = re.findall("\d+", c.id)
                    xp = int(index_x)
                    yp = int(index_y)
                    if str(c.text).find(str(DataGrid.raw_table[xp][yp])) == -1:
                        info_lbl.text = '[color=FF0000]Invalid Solution![/color]'
                        return
        info_lbl.text = '[color=32CD32]Victory![/color]'

    def hint(self,instance, **kwargs):
        if(DataGrid.hints):
            childs = self.parent.children

            def check(childs,random_index_x,random_index_y,my_id):
                done = False
                sol = str(DataGrid.solution[random_index_x][random_index_y])
                for ch in childs:
                    for c in ch.children:                        
                        if(str(c.id) == my_id and not DataGrid.hints_all):
                            if(c.text[14:-8] != sol):
                                c.state = "normal" 
                                c.text = '[color=000000]' + sol + '[/color]'
                                DataGrid.solution[random_index_x][random_index_y] = "OK"
                                return True
                        elif(str(c.id) == my_id and DataGrid.hints_all):
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
                    my_id = "x_" + str(random_index_x) + "_" + str(random_index_y)
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
            if DataGrid.all_sel:
                if keycode == 76:  # Deleted pressed!
                    for ch in DataGrid.childs:
                        for c in ch.children:
                            if c.id[:1] == 'x':
                                c.state = "normal"
                                c.text = '[color=000000][/color]'
                DataGrid.all_sel = False
                DataGrid.solution = [row[:] for row in DataGrid.raw_table]
                DataGrid.count = 0
            elif text and DataGrid.obj.state == "down":
                if text.isdigit():
                    loc = list(DataGrid.obj.id[2:])
                    x = int(loc[0])
                    y = int(loc[2])
                    if DataGrid.validate:
                        if DataGrid.raw_table[x][y].as_string() == text:
                            DataGrid.obj.state = "normal"
                            DataGrid.obj.text = '[color=000000]' + text + '[/color]'
                            DataGrid.solution[x][y] = "OK"
                        else:
                            DataGrid.obj.state = "normal"
                            DataGrid.obj.text = '[color=FF0000]' + text + '[/color]'
                    else:
                        DataGrid.obj.state = "normal"
                        DataGrid.obj.text = '[color=000000]' + text + '[/color]'

            elif keycode == 76 and DataGrid.obj.state == "down": # Deleted pressed!
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
        size= int(DataGrid.board_size)
        res = generate_board.generate(size, 0)

        complete_board(res[0])
        self.cols = len(res[0][1])
        self.rows = len(res[0])
        self.spacing = [1, 1]
        for row in range(len(res[0])):
            self.add_row(res[0][row], calculate_col_size(len(res[0])),self)
        DataGrid.solution = res[1]
        DataGrid.raw_table = [row[:] for row in res[1]]

    def __init__(self, body_data, **kwargs):
        super(DataGrid, self).__init__(**kwargs)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        if body_data:
            self.cols = len(body_data[1])
            self.rows = len(body_data)
            self.spacing = [1, 1]

            for row in range(len(body_data)):
                self.add_row(body_data[row], calculate_col_size(len(body_data)), self)

###
checkbox1 = DataGrid.validate
checkbox2 = DataGrid.hints
checkbox3 = DataGrid.hints_all
board_size_input = DataGrid.board_size


def settings_panel(self):
    info_lbl.text = 'MathemaGrids puzzle'
    global checkbox1
    global checkbox2
    global checkbox3
    global board_size_input

    def on_checkbox_active(checkbox, value):
        if checkbox.id == "ck_validate":
            global checkbox1
            checkbox1 = value
        elif checkbox.id == "ck_hints":
            global checkbox2
            checkbox2 = value
        elif checkbox.id == "ck_hints_all":
            global checkbox3
            checkbox3 = value

    def save_settings(self):
        DataGrid.validate = checkbox1
        DataGrid.hints = checkbox2
        DataGrid.hints_all = checkbox3
        DataGrid.board_size = size_input.text

    label1 = Label(text='Validate moves in real time', id="lbl_validate")
    label2 = Label(text='Enable hints', id="lbl_hints")
    label3 = Label(text='Hints only fill empty spaces', id="lbl_hints_all")
    label4 = Label(text='Choose generated board size', id='board_size_input')
    check1 = CheckBox(id="ck_validate", active=DataGrid.validate)
    check2 = CheckBox(id="ck_hints", active=DataGrid.hints)
    check3 = CheckBox(id="ck_hints_all", active=DataGrid.hints_all)
    check1.bind(active=on_checkbox_active)
    check2.bind(active=on_checkbox_active)
    check3.bind(active=on_checkbox_active)

    size_input = Spinner(text=DataGrid.board_size, values=('2', '3', '4'), size=(100, 44))
    size_input.is_open

    settings_grid = GridLayout(cols=2)
    settings_grid.add_widget(label1)
    settings_grid.add_widget(check1)
    settings_grid.add_widget(label2)
    settings_grid.add_widget(check2)
    settings_grid.add_widget(label3)
    settings_grid.add_widget(check3)
    settings_grid.add_widget(label4)
    settings_grid.add_widget(size_input)

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
board = generate_board.generate(2, 0)
complete_board(board[0])

# Declaration of the grid object
grid = DataGrid(board[0])
grid.rows = len(board[0])

DataGrid.solution = board[1]
DataGrid.raw_table = [row[:] for row in board[1]]

scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x': .5, 'center_y': .5})
scroll.add_widget(grid)
scroll.do_scroll_y = True
scroll.do_scroll_x = False

open_btn = Button(text="Open puzzle", on_press=partial(grid.open))
generate_btn = Button(text="Generate puzzle", on_press=partial(grid.generate))
select_all_btn = Button(text="Select All", on_press=partial(grid.select_all))
unselect_all_btn = Button(text="Unselect All", on_press=partial(grid.unselect_all))
hint_btn = Button(text="Hint", on_press=partial(grid.hint))
validate_btn = Button(text="Validate", on_press=partial(grid.validate))
settings_btn = Button(text="Settings", on_press=settings_panel)

info_lbl = Label(text='MathemaGrids puzzle', id="lbl_info", markup=True)

btn_grid = BoxLayout(orientation="vertical")
btn_grid.add_widget(open_btn)
btn_grid.add_widget(generate_btn)
btn_grid.add_widget(select_all_btn)
btn_grid.add_widget(unselect_all_btn)
btn_grid.add_widget(hint_btn)
btn_grid.add_widget(validate_btn)
btn_grid.add_widget(settings_btn)
btn_grid.add_widget(info_lbl)

root = BoxLayout(orientation="horizontal")

root.add_widget(scroll)
root.add_widget(btn_grid)

class MathemaGridsApp(App):
    def build(self):
        return root

if __name__ == '__main__':
    MathemaGridsApp().run()