import sqlite3
import tkinter as tk
from math import ceil

import account_management
import event_management
import global_variables
import pc_identifier
import screen_users


class Results(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.navbarGrid = tk.Frame(self, padx=10, pady=10)
        self.navbarGrid.grid(row=0, column=0)

        self.homeButton = tk.Button(self.navbarGrid, text="Home", font=global_variables.text(), command=self.controller.show_home)
        self.homeButton.grid(row=0, column=1)

        self.databaseButton = tk.Button(self.navbarGrid, text="Database", font=global_variables.text(), command=self.controller.show_database)
        self.databaseButton.grid(row=0, column=2)

        self.resultsButton = tk.Button(self.navbarGrid, text="Results", font=global_variables.text())
        self.resultsButton.grid(row=0, column=3)

        self.mainScreenGrid = tk.Frame(self)
        self.mainScreenGrid.grid(row=2, column=0, columnspan=4)

        self.descriptionLabel = tk.Label(self.mainScreenGrid, text="Select teams to compare", font=global_variables.text())
        self.descriptionLabel.grid(row=1, column=0)

        self.showTeamButton = tk.Button(self.mainScreenGrid, text="Show highlighted team details", font=global_variables.text(14))
        self.showTeamButton.grid(row=2, column=0)

        self.compareSelectedButton = tk.Button(self.mainScreenGrid, text="Compare selected teams", font=global_variables.text(14))
        self.compareSelectedButton.grid(row=3, column=0)

        self.dataBox = tk.Listbox(self.mainScreenGrid, width=150, height=45)
        self.dataBox.grid(row=1, column=1, rowspan=8)
        self.dataBox.config(font=("Courier", 12))

    def bindSetup(self):
        pass