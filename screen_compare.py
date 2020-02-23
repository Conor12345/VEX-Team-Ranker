import tkinter as tk


class Compare(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

    def bindSetup(self):
        pass