import sqlite3
import tkinter as tk
from math import ceil

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

        #TODO add user creation screens

    def show_events(self):
        if self.currentPage is not None:
            self.currentPage.grid_forget()
        self.currentPage = GeneralData(self, "tblEvents")
        self.currentPage.grid(row=3, column=0, columnspan=5)

    def show_matches(self):
        self.currentPage.grid_forget()
        self.currentPage = GeneralData(self, "tblMatches")
        self.currentPage.grid(row=3, column=0, columnspan=5)

    def show_teams(self):
        self.currentPage.grid_forget()
        self.currentPage = GeneralData(self, "tblTeams")
        self.currentPage.grid(row=3, column=0, columnspan=5)

    def show_users(self):
        if self.controller.isAdmin:
            self.currentPage.grid_forget()
            self.currentPage = GeneralData(self, "tblUsers")
            self.currentPage.grid(row=3, column=0, columnspan=5)
        else:
            errorLabel = tk.Label(self.smallMenu, text="ERROR - Insufficient permissions", font=global_variables.text(16))
            errorLabel.grid(row=1, column=4)


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

        self.rowWidth = int(150 / len(self.columnNames))

        tableName = tk.Label(self, text=tblName + " - Search", font=global_variables.text())
        tableName.grid(row=0, column=0, columnspan=2)

        startRow = 1
        self.searchBoxes = []
        for searchItem in range(len(self.columnNames)):
            label = tk.Label(self, text=self.columnNames[searchItem], font=global_variables.text(14))
            label.grid(row=searchItem + startRow, column=0)

            self.searchBoxes.append(tk.Entry(self, font=global_variables.text(14)))
            self.searchBoxes[searchItem].grid(row=searchItem + startRow, column=1)

        self.refreshButton = tk.Button(self, text="Search", font=global_variables.text(14), command=self.updateData)
        self.refreshButton.grid(row=len(self.columnNames) + 1, column=0, columnspan=2)

        self.dataBox = tk.Listbox(self, width=150, height=20)
        self.dataBox.grid(row=1, column=2, rowspan=10)
        self.dataBox.config(font=global_variables.text(12))

        self.updateData()

    def updateData(self):
        noSearches = True
        searches = []
        for searchTerm in self.searchBoxes:
            if searchTerm.get() != "":
                noSearches = False
            searches.append(searchTerm.get())

        query = "SELECT * FROM " + self.tblName
        if not noSearches:
            first = True
            for i in range(0, len(searches)):
                if first:
                    if searches[i] != "":
                        query += " WHERE " + self.columnNames[i] + " = '" + searches[i] + "'"
                        first = False
                else:
                    if searches[i] != "":
                        query += " AND " + self.columnNames[i] + " = '" + searches[i] + "'"

        db = sqlite3.connect("database.db")
        c = db.cursor()
        results = c.execute(query).fetchall()

        self.dataBox.delete(0, tk.END)
        row = ""
        for header in self.columnNames:
            row += str(header).ljust(self.rowWidth, " ")
        self.dataBox.insert(tk.END, row)
        self.dataBox.insert(tk.END, "")

        for result in results: #TODO stop printing user password hashes
            rows = [""]
            for record in result:
                if len(str(record)) <= self.rowWidth:
                    rows[0] += str(record).ljust(self.rowWidth, " ")
                else:
                    longestRecord = global_variables.longestStringInArray(result)
                    rowsNeeded = int(ceil((longestRecord / self.rowWidth))) + 1
                    rows = ["" for i in range(rowsNeeded)]
                    for i in range(len(result)):
                        if len(str(result[i])) <= self.rowWidth:
                            rows[0] += str(result[i]).ljust(self.rowWidth, " ")
                            for j in range(1, rowsNeeded):
                                rows[j] += self.rowWidth * " "
                        else:
                            toPlace = result[i].split(" ")
                            for k in range(rowsNeeded):
                                currentLine = ""
                                while len(toPlace) > 0:
                                    if len(currentLine + toPlace[0]) <= self.rowWidth:
                                        currentLine += toPlace[0] + " "
                                        del toPlace[0]
                                    else:
                                        rows[k] += currentLine.ljust(self.rowWidth, " ")
                                        currentLine = ""
                                        break
                                if currentLine != "":
                                    rows[k] += currentLine.ljust(self.rowWidth, " ")
                    break

            for row in rows:
                if not global_variables.isOnlySpaces(row):
                    self.dataBox.insert(tk.END, row)
