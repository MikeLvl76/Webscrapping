from tkinter import Button, Canvas, Entry, Label, Tk
import tkinter
from tkinter.ttk import Combobox

class Tools:

    def __init__(self) -> None:
        self.root = None
        self.dimensions = ()

    def create_window(self, title, dimensions = ()):
        self.root = Tk()
        self.root.title(title)
        if len(dimensions) == 2:
            width = dimensions[0]
            height = dimensions[1]
        else:
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
        self.dimensions = (width, height)
        self.root.geometry('x'.join((str(width), str(height))))
    
    def create_canvas(self, master, dimensions = (), **args):
        canvas = None
        if len(dimensions) == 2:
            canvas = Canvas(master, width=dimensions[0], height=dimensions[1], **args)
        else:
            canvas = Canvas(master, width=self.dimensions[0], height=self.dimensions[1], **args)
        canvas.pack()
        return canvas

    def add_stringvar(self):
        return tkinter.StringVar()

    def add_entry(self, master, string_var, **args):
        entry = Entry(master, textvariable=string_var, **args)
        entry.pack()
        return entry

    def add_button(self, master, text, command, **args):
        button = Button(master, text=text, command=command, **args)
        button.pack()
        return button

    def add_label(self, master, text, **args):
        label = Label(master, text=text, **args)
        label.pack()
        return label

    def add_combobox(self, master, values = [], **args):
        combobox = Combobox(master, values=values, **args)
        combobox.pack()
        return combobox
    
    # use this
    def place(self, arg={}):
        for key in arg.keys():
            value = arg[key]
            value[0].place(x=value[1], y=value[2], width=value[3], height=value[4])

    def place_items(self, items, x_serie, y_serie, w_serie, h_serie):
        for item, x, y, w, h in zip(items, x_serie, y_serie, w_serie, h_serie):
            item.place(x=x, y=y, width=w, height=h)

    def bind(self, item, type, callback):
        item.bind(type, callback)

    def change_state(self, item, state):
        item['state'] = state

    def loop(self):
        self.root.mainloop()

tools = Tools()
tools.create_window('Test')
canvas = tools.create_canvas(tools.root, (), background='red')
var = tools.add_stringvar()
entry = tools.add_entry(tools.root, var)
def show():
    print(var.get())
def test(event):
    print('New element selected')
button = tools.add_button(tools.root, 'Test', show)
combobox = tools.add_combobox(tools.root, [str(i) for i in range(10)])
tools.place_items([entry, button, combobox], [200, 400, 300], [200, 200, 500], [150, 50, 30], [20, 50, 20])
tools.bind(combobox, "<<ComboboxSelected>>", test)
tools.change_state(button, 'disabled')
tools.loop()
