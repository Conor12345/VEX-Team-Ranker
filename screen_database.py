import sqlite3
import tkinter as tk
from math import ceil

import account_management
import event_management
import global_variables
import screen_users


class Database(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.currentPage = None
        self.switch = None

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

    def show_new_users(self):
        self.currentPage.grid_forget()
        self.currentPage = screen_users.NewUser(self)
        self.currentPage.grid(row=3, column=0, columnspan=5)

    def show_update_users(self, UserName):
        self.currentPage.grid_forget()
        self.currentPage = screen_users.UpdateUser(self, UserName)
        self.currentPage.grid(row=3, column=0, columnspan=5)

class GeneralData(tk.Frame):
    def __init__(self, parent, tblName):
        tk.Frame.__init__(self, parent)

        self.parent = parent
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

        commaLabel = tk.Label(self, text="Use commas to separate search terms", font=global_variables.text(12))
        commaLabel.grid(row=1, column=0, columnspan=2)

        self.startRow = 2
        self.searchBoxes = []
        for searchItem in range(len(self.columnNames)):
            label = tk.Label(self, text=self.columnNames[searchItem], font=global_variables.text(14))
            label.grid(row=searchItem + self.startRow, column=0)

            self.searchBoxes.append(tk.Entry(self, font=global_variables.text(14)))
            self.searchBoxes[searchItem].grid(row=searchItem + self.startRow, column=1)

        self.refreshButton = tk.Button(self, text="Search", font=global_variables.text(14), command=self.updateData)
        self.refreshButton.grid(row=len(self.columnNames) + 2, column=0, columnspan=2)

        if self.parent.switch is not None:
            self.searchBoxes[0].insert(0, self.parent.switch)
            self.parent.switch = None

        self.startRow = len(self.columnNames) + 3  # Increment after each use

        if self.tblName == "tblEvents":
            self.refreshButton = tk.Button(self, text="Update recent events", font=global_variables.text(14), command=self.refreshEventData)
            self.refreshButton.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

            self.showMatches = tk.Button(self, text="Show corresponding matches", font=global_variables.text(14), command=self.switchToMatchView)
            self.showMatches.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

        elif self.tblName == "tblMatches":
            self.showEvents = tk.Button(self, text="Show corresponding event", font=global_variables.text(14), command=self.switchToEventView)
            self.showEvents.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

        elif self.tblName == "tblTeams":
            pass

        elif self.tblName == "tblUsers":
            self.newUserButton = tk.Button(self, text="New user", font=global_variables.text(14), command=self.parent.show_new_users)
            self.newUserButton.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

            self.updateUserButton = tk.Button(self, text="Update user", font=global_variables.text(14), command=self.updateUserScreen)
            self.updateUserButton.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

        self.dataBox = tk.Listbox(self, width=150, height=40)
        self.dataBox.grid(row=1, column=2, rowspan=20)
        self.dataBox.config(font=("Courier", 12))

        self.updateData()

    def updateData(self):
        noSearches = True
        searches = []
        for searchTerm in self.searchBoxes:
            if searchTerm.get() != "":
                noSearches = False
            searches.append(searchTerm.get().replace(" ", "").split(","))

        query = "SELECT * FROM " + self.tblName
        if not noSearches:
            first = True
            for i in range(0, len(searches)):
                if first:
                    if searches[i][0] != "":
                        for searchTerm in searches[i]:
                            if len(searches[i]) > 1:
                                if searchTerm == searches[i][0]: # If its the search first term
                                    query += " WHERE (" + self.columnNames[i] + " LIKE '%" + searchTerm + "%'"
                                    first = False
                                else:
                                    query += " OR " + self.columnNames[i] + " LIKE '%" + searchTerm + "%'"
                            else:
                                query += " WHERE " + self.columnNames[i] + " LIKE '%" + searchTerm + "%'"
                                first = False
                        if len(searches[i]) > 1:
                            query += ")"
                else:
                    if searches[i][0] != "":
                        for searchTerm in searches[i]:
                            if len(searches[i]) > 1:
                                if searchTerm == searches[i][0]: # If its the search first term
                                    query += " AND (" + self.columnNames[i] + " LIKE '%" + searchTerm + "%'"
                                    first = False
                                else:
                                    query += " OR " + self.columnNames[i] + " LIKE '%" + searchTerm + "%'"
                            else:
                                query += " AND " + self.columnNames[i] + " LIKE '%" + searchTerm + "%'"
                                first = False
                        if len(searches[i]) > 1:
                            query += ")"

        if self.tblName == "tblEvents":
            query += " ORDER BY Date DESC"

        elif self.tblName == "tblMatches":
            query += " ORDER BY EventID DESC, MatchLevel ASC, MatchNum ASC"

        elif self.tblName == "tblTeams":
            query += " ORDER BY TeamNum"

        elif self.tblName == "tblUsers":
            query += " ORDER BY UserID"

        db = sqlite3.connect("database.db")
        c = db.cursor()
        results = c.execute(query).fetchall()

        self.dataBox.delete(0, tk.END)
        row = ""
        for header in self.columnNames:
            row += str(header).ljust(self.rowWidth, " ")
        self.dataBox.insert(tk.END, row)
        self.dataBox.insert(tk.END, "")

        for result in results:
            rows = [""]
            for record in result:
                if len(str(record)) <= self.rowWidth:
                    rows[0] += str(record).ljust(self.rowWidth, " ")
                else:
                    longestRecord = global_variables.longestStringInArray(result)
                    rowsNeeded = int(ceil((longestRecord / self.rowWidth))) + 1
                    rows = ["" for i in range(rowsNeeded)]
                    for i in range(len(result)):
                        if len(str(result[i])) <= self.rowWidth - 2:
                            rows[0] += str(result[i]).ljust(self.rowWidth, " ")
                            for j in range(1, rowsNeeded):
                                rows[j] += self.rowWidth * " "
                        else:
                            toPlace = result[i].split(" ")
                            for k in range(rowsNeeded):
                                currentLine = ""
                                while len(toPlace) > 0:
                                    if len(currentLine + toPlace[0]) <= self.rowWidth - 2:
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

    def refreshEventData(self):
        event_management.refresh_recent_events()
        self.updateData()

    def switchToMatchView(self):
        selectedEventID = self.dataBox.selection_get()[0:14]
        if global_variables.isOnlySpaces([selectedEventID]):
            errorLabel = tk.Label(self, text="ERROR - Select record with an EventID", font=global_variables.text(12))
            errorLabel.grid(row=self.startRow, column=0, columnspan=2)
        else:
            self.parent.switch = selectedEventID
        self.parent.show_matches()

    def switchToEventView(self):
        self.parent.switch = self.dataBox.selection_get()[0:14]
        self.parent.show_events()

    def updateUserScreen(self):
        UserName = self.dataBox.selection_get()[self.rowWidth:2 * self.rowWidth].strip()
        if not account_management.get_user_data(UserName):
            errorLabel = tk.Label(self, text="ERROR - Select a user to update", font=global_variables.text(12))
            errorLabel.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1
        else:
            self.parent.show_update_users(UserName)