import sqlite3
import tkinter as tk

import global_variables


class Database(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.currentPage = None

        self.navbarGrid = tk.Frame(self, padx=10, pady=10)
        self.navbarGrid.grid(row=0, column=0)

        self.homeButton = tk.Button(self.navbarGrid, text="Home", font=global_variables.text(), command=self.controller.show_home)
        self.homeButton.grid(row=0, column=1)

        self.databaseButton = tk.Button(self.navbarGrid, text="Database", font=global_variables.text())
        self.databaseButton.grid(row=0, column=2)

        self.resultsButton = tk.Button(self.navbarGrid, text="Results", font=global_variables.text())
        self.resultsButton.grid(row=0, column=3)

        self.smallMenu = tk.Frame(self, padx=10, pady=10)
        self.smallMenu.grid(row=1, column=0)

        self.eventButton = tk.Button(self.smallMenu, text="Events", command=self.show_events, font=global_variables.text(16))
        self.eventButton.grid(row=1, column=0)

        self.matchButton = tk.Button(self.smallMenu, text="Matches", command=self.show_matches, font=global_variables.text(16))
        self.matchButton.grid(row=1, column=1)

        self.teamButton = tk.Button(self.smallMenu, text="Teams", command=self.show_teams, font=global_variables.text(16))
        self.teamButton.grid(row=1, column=2)

        self.userButton = tk.Button(self.smallMenu, text="Users", command=self.show_users, font=global_variables.text(16))
        self.userButton.grid(row=1, column=3)

        self.show_events()

    def show_events(self):
        if self.currentPage is not None:
            self.currentPage.grid_forget()
        self.currentPage = GeneralData(self, "tblEvents")
        self.currentPage.grid(row=3, column=0)

    def show_matches(self):
        self.currentPage.grid_forget()
        self.currentPage = GeneralData(self, "tblMatches")
        self.currentPage.grid(row=3, column=0)

    def show_teams(self):
        self.currentPage.grid_forget()
        self.currentPage = GeneralData(self, "tblTeams")
        self.currentPage.grid(row=3, column=0)

    def show_users(self):
        if self.controller.isAdmin:
            self.currentPage.grid_forget()
            self.currentPage = GeneralData(self, "tblUsers")
            self.currentPage.grid(row=3, column=0)
        else:
            print("Error - Insufficient permissions")
            #TODO make proper error message


class GeneralData(tk.Frame):
    def __init__(self, parent, tblName):
        tk.Frame.__init__(self, parent)

        self.tblName = tblName
        self.columnNames = []

        db = sqlite3.connect("database.db")  #
        c = db.cursor()
        columnNames = c.execute("PRAGMA table_info(" + self.tblName + ")").fetchall()
        for column in columnNames:
            self.columnNames.append(column[1])

        tableName = tk.Label(self, text=tblName + " - Search", font=global_variables.text())
        tableName.grid(row=0, column=0, columnspan=2)

        startRow = 1
        self.searchBoxes = []
        for searchItem in range(len(self.columnNames)):
            label = tk.Label(self, text=self.columnNames[searchItem], font=global_variables.text(12))
            label.grid(row=searchItem + startRow, column=0)

            self.searchBoxes.append(tk.Entry(self, font=global_variables.text(12), command=self.updateSearch))
            self.searchBoxes[searchItem].grid(row=searchItem + startRow, column=1)

    def updateSearch(self):
        pass