from tkinter import Canvas, Entry, Tk
import tkinter

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
            self.dimensions = (width, height)
            self.root.geometry('x'.join((str(width), str(height))))
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

    def add_entry(self, master, string_var, **args):
        entry = Entry(master, textvariable=string_var, **args)
        entry.pack()
        return entry

    def place_items(self, items, x_serie, y_serie, w_serie, h_serie):
        for item, x, y, w, h in zip(items, x_serie, y_serie, w_serie, h_serie):
            item.place(x=x, y=y, width=w, height=h)

    def loop(self):
        self.root.mainloop()

tools = Tools()
tools.create_window('Test')
canvas = tools.create_canvas(tools.root, (), background='red')
var = tkinter.StringVar()
entry = tools.add_entry(tools.root, var)
tools.place_items([entry], [200], [200], [150], [20])
tools.loop()