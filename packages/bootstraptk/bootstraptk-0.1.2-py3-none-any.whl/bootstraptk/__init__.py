from tkinter import *
import os

class toolbar(Frame):
    def __init__(self, parent = None, **kw):
        Frame.__init__(self, parent, **kw)
        self.root = parent
    
    def add_button(self, text="", background="white", foreground="black", bd="0", height=0, side="left", fill="x"):
        Button(self, text=text, background=background, foreground=foreground, bd=bd, height=height).pack(side=side, fill=fill)

class filelist(Listbox):
    def __init__(self, parent = None, **kw):
        Listbox.__init__(self, parent, **kw)
        self.root = parent
    
    def add_files(self, folder):
        files = os.listdir(folder)
        for file in files:
            self.insert(1, file)

class theme():
    def __init__(self, master):
        self.master = master

    def dark(self, bg="", fg=""):
        widgets = self.master.winfo_children()
        for widget in widgets:
            widget.config(bg="#444444", fg="white")

    def custom(self, bg="white", fg="black"):
        widgets = self.master.winfo_children()
        for widget in widgets:
            widget.config(bg=bg, fg=fg)

