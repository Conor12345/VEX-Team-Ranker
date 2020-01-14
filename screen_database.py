import sqlite3
import tkinter as tk
from math import ceil

import account_management
import event_management
import global_variables
import pc_identifier
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

        self.resultsButton = tk.Button(self.navbarGrid, text="Results", font=global_variables.text(), command=self.controller.show_results)
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
        self.bindSetup()

    def show_matches(self):
        self.currentPage.grid_forget()
        self.currentPage = GeneralData(self, "tblMatches")
        self.currentPage.grid(row=3, column=0, columnspan=5)
        self.bindSetup()

    def show_teams(self):
        self.currentPage.grid_forget()
        self.currentPage = GeneralData(self, "tblTeams")
        self.currentPage.grid(row=3, column=0, columnspan=5)
        self.bindSetup()

    def show_users(self):
        if self.controller.isAdmin:
            self.currentPage.grid_forget()
            self.currentPage = GeneralData(self, "tblUsers")
            self.currentPage.grid(row=3, column=0, columnspan=5)
            self.bindSetup()
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

    def bindSetup(self):
        self.controller.bind("<Return>", self.currentPage.updateData)

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

        if pc_identifier.getPC() == "BadLaptop":
            tempWidth = 100
        else:
            tempWidth = 150

        self.columnWidth = int(tempWidth / len(self.columnNames)) # Calculate the maximum column width

        tableName = tk.Label(self, text=tblName + " - Search", font=global_variables.text())
        tableName.grid(row=0, column=0, columnspan=2)

        commaLabel = tk.Label(self, text="Use commas to separate search terms", font=global_variables.text(12))
        commaLabel.grid(row=1, column=0, columnspan=2)

        self.startRow = 2
        self.searchBoxes = []
        self.labels = []
        for searchItem in range(len(self.columnNames)):
            if self.columnNames[searchItem] not in ["RedTeam1","RedTeam2", "BlueTeam1", "BlueTeam2"]:
                self.labels.append(tk.Label(self, text=self.columnNames[searchItem], font=global_variables.text(14)))
                self.labels[self.startRow - 2].grid(row=self.startRow, column=0)

                self.searchBoxes.append(tk.Entry(self, font=global_variables.text(14)))
                self.searchBoxes[self.startRow - 2].grid(row=self.startRow, column=1)

                self.startRow += 1

        if self.tblName == "tblMatches":
            self.labels.append(tk.Label(self, text="TeamNumber", font=global_variables.text(14)))
            self.labels[self.startRow - 2].grid(row=self.startRow, column=0)

            self.searchBoxes.append(tk.Entry(self, font=global_variables.text(14)))
            self.searchBoxes[self.startRow - 2].grid(row=self.startRow, column=1)

            self.startRow += 1

        self.refreshButton = tk.Button(self, text="Search", font=global_variables.text(14), command=self.updateData)
        self.refreshButton.grid(row=self.startRow, column=0, columnspan=2)

        self.startRow += 1

        if self.parent.switch is not None:
            self.searchBoxes[self.parent.switch[1]].insert(0, self.parent.switch[0])
            self.parent.switch = None

        if self.tblName == "tblEvents":
            self.refreshButton = tk.Button(self, text="Update recent events", font=global_variables.text(14), command=self.refreshEventData)
            self.refreshButton.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

            self.showMatches = tk.Button(self, text="Show corresponding matches", font=global_variables.text(14), command=self.switchToMatchViewEvent)
            self.showMatches.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

        elif self.tblName == "tblMatches":
            self.showEvents = tk.Button(self, text="Show corresponding event", font=global_variables.text(14), command=self.switchToEventView)
            self.showEvents.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

        elif self.tblName == "tblTeams":
            self.showMatches = tk.Button(self, text="Show corresponding matches", font=global_variables.text(14), command=self.switchToMatchViewTeam)
            self.showMatches.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

        elif self.tblName == "tblUsers":
            self.newUserButton = tk.Button(self, text="New user", font=global_variables.text(14), command=self.parent.show_new_users)
            self.newUserButton.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

            self.updateUserButton = tk.Button(self, text="Update user", font=global_variables.text(14), command=self.updateUserScreen)
            self.updateUserButton.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1

        self.dataBox = tk.Listbox(self, width=tempWidth, height=40)
        self.dataBox.grid(row=1, column=2, rowspan=20)
        self.dataBox.config(font=("Courier", 12))

        self.updateData()

    def updateData(self, test=None):
        noSearches = True
        searches = []
        for searchTerm in self.searchBoxes:
            if searchTerm.get() != "":
                noSearches = False
            currentSearches = [] # Sets up temporary list where items can be put
            for searchItem in searchTerm.get().split(","): # Iterate through comma separated values
                currentSearches.append(searchItem.strip()) # Adds item to temp list without spaces at ends
            searches.append(currentSearches) # Adds temp list to make search array


        query = "SELECT * FROM " + self.tblName
        if not noSearches:
            first = True
            for searchBox in range(0, len(searches)):
                if searches[searchBox][0] != "": # If the search box isn't empty
                    if first: # First search query uses WHERE
                        query += " WHERE "
                        first = False
                    else: # Subsequent searches uses AND
                        query += " AND "

                    subquery = "" # The query for this box goes in here
                    for searchTerm in searches[searchBox]: # Iterates through all searches in each box
                        if searchTerm != searches[searchBox][0]:  # If its not the first term
                            subquery += " OR "
                        if self.labels[searchBox]["text"] != "TeamNumber":  # If its not the special case teams
                            subquery += self.labels[searchBox]["text"] + " LIKE '%" + searchTerm + "%'"
                        else:  # It is the special case for teams on match screen
                            subquery += "("
                            for columnName in ["RedTeam1", "RedTeam2", "BlueTeam1", "BlueTeam2"]:  # Iterate through team column names
                                if columnName != "RedTeam1":  # If its not the first column
                                    subquery += " OR "
                                subquery += columnName + " LIKE '%" + searchTerm + "%'"
                            subquery += ")"

                    query = query + "(" + subquery + ")" # Puts subquery into main query with brackets

        # Orders data using specific values per table
        if self.tblName == "tblEvents":
            query += " ORDER BY Date DESC"

        elif self.tblName == "tblMatches":
            query += " ORDER BY EventID DESC, MatchLevel ASC, MatchNum ASC"

        elif self.tblName == "tblTeams":
            query += " ORDER BY TeamNum"

        elif self.tblName == "tblUsers":
            query += " ORDER BY UserID"

        print(query)

        db = sqlite3.connect("database.db")
        c = db.cursor()
        results = c.execute(query).fetchall()

        self.dataBox.delete(0, tk.END) # Clears databox
        row = ""
        for header in self.columnNames: # Adds headers to table
            row += str(header).ljust(self.columnWidth, " ")
        self.dataBox.insert(tk.END, row) # Inserts header row
        self.dataBox.insert(tk.END, " ") # Inserts empty row for spacing

        for result in results: # Iterates through each record
            rows = [""]
            for record in result: # Iterates though each column
                if len(str(record)) <= self.columnWidth: # If the data fits in the space without wrapping
                    rows[0] += str(record).ljust(self.columnWidth, " ") # Adds record with padding on right to fill space
                else: # If the data doesn't fit in the space, line wrapping
                    longestRecord = global_variables.longestStringInArray(result) # Finds the longest string in this result
                    rowsNeeded = int(ceil((longestRecord / self.columnWidth))) + 1 # Calculates the MAXIMUM number of rows needed
                    rows = ["" for i in range(rowsNeeded)] # Generates array of rows
                    for i in range(len(result)): # Iterates through the records
                        if len(str(result[i])) <= self.columnWidth - 2: # If the record can fit in the column
                            rows[0] += str(result[i]).ljust(self.columnWidth, " ") # Places record into column with right padding
                            for j in range(1, rowsNeeded): # Iterates through the row cache
                                rows[j] += self.columnWidth * " " # Fills each line with spaces to fill gap
                        else: # If the record cannot fit into the column
                            toPlace = result[i].split(" ") # Splits the record into array of words
                            for k in range(rowsNeeded): # Iterates through row cache
                                currentLine = ""
                                while len(toPlace) > 0: # Continues until there are no more words to place or line is full
                                    if len(currentLine + toPlace[0]) <= self.columnWidth - 2: # If next word can fit onto current line
                                        currentLine += toPlace[0] + " " # Adds word to line
                                        del toPlace[0] # Removes word from word arraty
                                    else: # If the next word cannot fit into current line
                                        rows[k] += currentLine.ljust(self.columnWidth, " ") # Adds current line to row cache
                                        currentLine = "" # Clears line cache
                                        break # Stops while loop as line is full
                                if currentLine != "": # If no data could fit onto line e.g. password hash
                                    rows[k] += currentLine.ljust(self.columnWidth, " ") # Adds blank line of correct width
                    break # Moves onto next result

            for row in rows: # Iterates through each row in cacge
                if not global_variables.isOnlySpaces(row): # Ensure row is not all blank
                    self.dataBox.insert(tk.END, row) # Inserts row into table

    def refreshEventData(self):
        event_management.refresh_recent_events()
        self.updateData()

    def switchToMatchViewEvent(self):
        selectedEventID = self.dataBox.selection_get()[0:14]
        if global_variables.isOnlySpaces([selectedEventID]):
            errorLabel = tk.Label(self, text="ERROR - Select record with an EventID", font=global_variables.text(12))
            errorLabel.grid(row=self.startRow, column=0, columnspan=2)
        else:
            self.parent.switch = [selectedEventID, 0]
        self.parent.show_matches()

    def switchToEventView(self):
        self.parent.switch = [self.dataBox.selection_get()[0:14], 0]
        self.parent.show_events()

    def switchToMatchViewTeam(self):
        self.parent.switch = [self.dataBox.selection_get()[0:20].strip(), 5]
        self.parent.show_matches()

    def updateUserScreen(self):
        UserName = self.dataBox.selection_get()[self.columnWidth:2 * self.columnWidth].strip()
        if not account_management.get_user_data(UserName):
            errorLabel = tk.Label(self, text="ERROR - Select a user to update", font=global_variables.text(12))
            errorLabel.grid(row=self.startRow, column=0, columnspan=2)
            self.startRow += 1
        else:
            self.parent.show_update_users(UserName)