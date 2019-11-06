import tkinter as tk

import global_variables


class Database(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.navbarGrid = tk.Frame(self, padx=10, pady=10)
        self.navbarGrid.grid(row=0, column=0)

        self.homeButton = tk.Button(self.navbarGrid, text="Home", font=global_variables.text(), command=self.controller.show_home)
        self.homeButton.grid(row=0, column=1)

        self.databaseButton = tk.Button(self.navbarGrid, text="Database", font=global_variables.text())
        self.databaseButton.grid(row=0, column=2)

        self.resultsButton = tk.Button(self.navbarGrid, text="Results", font=global_variables.text())
        self.resultsButton.grid(row=0, column=3)