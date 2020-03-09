import tkinter as tk

import api_query
import global_variables
import team_management


def get5thElement(array):
    return array[4]


def get6thElement(array):
    return array[5]


def get7thElement(array):
    return array[6]


class Results(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.navbarGrid = tk.Frame(self, padx=10, pady=10)
        self.navbarGrid.grid(row=0, column=0, rowspan=2)

        self.homeButton = tk.Button(self.navbarGrid, text="Home", font=global_variables.text(), command=self.controller.show_home)
        self.homeButton.grid(row=0, column=1)

        self.databaseButton = tk.Button(self.navbarGrid, text="Database", font=global_variables.text(), command=self.controller.show_database)
        self.databaseButton.grid(row=0, column=2)

        self.resultsButton = tk.Button(self.navbarGrid, text="Results", font=global_variables.text())
        self.resultsButton.grid(row=0, column=3)

        self.descriptionLabel = tk.Label(self, text="Select teams to compare", font=global_variables.text())
        self.descriptionLabel.grid(row=2, column=0, padx=10)

        self.showTeamButton = tk.Button(self, text="Show highlighted team details", font=global_variables.text(14), command=self.showTeamScreen)
        self.showTeamButton.grid(row=3, column=0)

        self.compareSelectedButton = tk.Button(self, text="Compare selected teams", font=global_variables.text(14), command=self.showCompareScreen  )
        self.compareSelectedButton.grid(row=4, column=0)

        self.fetchAwardDataButton = tk.Button(self, text="Collect award data", font=global_variables.text(14), command=self.fetchAwardData)
        self.fetchAwardDataButton.grid(row=5, column=0)

        self.dataBox = tk.Listbox(self, width=140, height=42)
        self.dataBox.grid(row=2, column=2, rowspan=20, columnspan=14)
        self.dataBox.config(font=("Courier", 12))

        self.tickBoxGrid = tk.Frame(self)
        self.tickBoxGrid.grid(row=2, column=1, rowspan=20, padx=10)

        selectLabel = tk.Label(self.tickBoxGrid, text="Selected?", font=global_variables.text(12))
        selectLabel.grid(row=0, column=0)

        self.tickBoxData = []
        self.tickBoxes = []
        for i in range(20):
            self.tickBoxData.append(tk.IntVar())
            self.tickBoxes.append(tk.Checkbutton(self.tickBoxGrid, variable=self.tickBoxData[i], command=self.updateSelectedBox))
            self.tickBoxes[-1].grid(row=i + 1, column=0, pady=7)

        self.upButton = tk.Button(self, text="   /\\   ", command=self.moveUp)  # Smallest to biggest
        self.upButton.grid(row=0, column=8, pady=10, columnspan=2)

        self.downButton = tk.Button(self, text="   \\/   ", command=self.moveDown)  # Biggest to smallest
        self.downButton.grid(row=30, column=8, pady=10, columnspan=2)

        self.sortBoxes = []
        temp = [tk.Button(self, text="\\/", command=lambda: self.reSortList(0, 0)),
                tk.Button(self, text="/\\", command=lambda: self.reSortList(0, 1))]

        temp[-2].grid(row=1, column=10, pady=5)
        temp[-1].grid(row=1, column=11, pady=5)
        self.sortBoxes.append(temp)

        temp = [tk.Button(self, text="\\/", command=lambda: self.reSortList(1, 0)),
                tk.Button(self, text="/\\", command=lambda: self.reSortList(1, 1))]

        temp[-2].grid(row=1, column=12, pady=5)
        temp[-1].grid(row=1, column=13, pady=5)
        self.sortBoxes.append(temp)

        temp = [tk.Button(self, text="\\/", command=lambda: self.reSortList(2, 0)),
                tk.Button(self, text="/\\", command=lambda: self.reSortList(2, 1))]

        temp[-2].grid(row=1, column=14, pady=5)
        temp[-1].grid(row=1, column=15, pady=5)
        self.sortBoxes.append(temp)

        self.sortBoxes[0][0]["relief"] = "sunken"

        selectedLabel = tk.Label(self, text="Currently selected teams:", font=global_variables.text(12))
        selectedLabel.grid(row=6, column=0)

        self.selectedDataBox = tk.Listbox(self, width=30, height=8)
        self.selectedDataBox.grid(row=7, column=0)
        self.selectedDataBox.config(font=("Courier", 12))

    def bindSetup(self):
        self.currentScreen = 0
        self.updateData()
        self.updateSelectedBox()

    def updateData(self):
        # Rank, Team Num, Team Name, Team City, Skill rating, Match win rate, Total awards

        self.display = []
        for team in set(self.controller.selectedTeams + [self.controller.teamNum]):
            tempArray = [None for x in range(7)]

            tempArray[1] = team
            tempArray[2] = team_management.get_team_name(team)
            tempArray[3] = team_management.get_team_city(team)
            tempArray[4] = round(team_management.get_team_skill(team), 3)

            if self.controller.teamDict is not None:
                winLossDraw = self.controller.teamDict[team][1]
                tempArray[5] = round((winLossDraw[0] + 0.5 * winLossDraw[2]) / sum(winLossDraw), 3)

            self.display.append(tempArray)

        self.display.sort(key=get5thElement, reverse=True)
        for i in range(len(self.display)):
            self.display[i][0] = i + 1

        self.updateScreen()

    def updateScreen(self):
        self.columnWidth = 20

        self.dataBox.delete(0, tk.END)  # Clears databox
        row = ""
        for header in ["Rank", "Team Number", "Team Name", "City", "Skill rating", "Match win rate", "Total awards won"]:  # Adds headers to table
            row += str(header).ljust(self.columnWidth, " ")
        self.dataBox.insert(tk.END, row)  # Inserts header row
        self.dataBox.insert(tk.END, " ")  # Inserts empty row for spacing

        for result in self.display[self.currentScreen * 20: (self.currentScreen + 1) * 20]:  # Iterates through each record
            row = ""
            for record in result:  # Iterates though each column
                if len(str(record)) <= self.columnWidth:  # If the data fits in the space without wrapping
                    row += str(record).ljust(self.columnWidth, " ")  # Adds record with padding on right to fill space
                else:
                    row += str(record)[:self.columnWidth - 1].ljust(self.columnWidth, " ")

            self.dataBox.insert(tk.END, row)  # Inserts row into table
            self.dataBox.insert(tk.END, " ")

        self.setButtonStates()

    def moveDown(self):
        if self.currentScreen < (len(self.display) / 20) - 1:
            self.storeButtonStates()
            self.currentScreen += 1
            self.updateScreen()

    def moveUp(self):
        if self.currentScreen != 0:
            self.storeButtonStates()
            self.currentScreen -= 1
            self.updateScreen()

    def fetchAwardData(self):
        for row in self.display:
            if self.controller.selectedSeason != "":
                row[6] = api_query.get_num_awards(row[1], self.controller.selectedSeason)
        self.updateScreen()

    def storeButtonStates(self, destructive=True):
        for i in range(0, 20):
            self.controller.buttonStates[i + 20 * self.currentScreen] = self.tickBoxData[i].get()
            if destructive:
                self.tickBoxData[i].set(0)

    def setButtonStates(self):
        for i in range(0, 20):
            self.tickBoxData[i].set(self.controller.buttonStates[i + 20 * self.currentScreen])

    def reSortList(self, col, direc):
        if self.display[0][4 + col] is None:  # Ensures the selected column has sortable data
            return False

        for column in self.sortBoxes:  # Unsink previous sort
            for button in column:
                if button["relief"] == "sunken":
                    button["relief"] = "raised"

        if direc == 0:
            state = True
        else:
            state = False

        if col == 0:
            self.display.sort(key=get5thElement, reverse=state)
        elif col == 1:
            self.display.sort(key=get6thElement, reverse=state)
        else:
            self.display.sort(key=get7thElement, reverse=state)

        self.sortBoxes[col][direc]["relief"] = "sunken"

        self.updateScreen()

    def updateSelectedBox(self):
        self.storeButtonStates(False)

        self.selectedForCompare = []
        for i in range(len(self.controller.buttonStates)):
            if self.controller.buttonStates[i] == 1:
                if i < len(self.display): # Ensures there is a result to select
                    self.selectedForCompare.append(self.display[i][0:2])

        self.selectedDataBox.delete(0, tk.END)  # Clears databox
        row = ""
        for header in ["Rank", "Team Number"]:  # Adds headers to table
            row += str(header).ljust(15, " ")
        self.selectedDataBox.insert(tk.END, row)  # Inserts header row
        self.selectedDataBox.insert(tk.END, " ")  # Inserts empty row for spacing

        for result in self.selectedForCompare:
            row = ""
            for record in result:  # Iterates though each column
                if len(str(record)) <= 15:  # If the data fits in the space without wrapping
                    row += str(record).ljust(15, " ")  # Adds record with padding on right to fill space
                else:
                    row += str(record)[:15 - 1].ljust(15, " ")
            self.selectedDataBox.insert(tk.END, row)  # Inserts row into table

    def showTeamScreen(self):
        teamNum = self.dataBox.get(tk.ACTIVE)
        if teamNum[0] != "R" and teamNum[0] != " ":
            self.controller.teamDisplay = teamNum[15:31].strip()
            self.controller.show_team()

    def showCompareScreen(self):
        if 2 <= len(self.selectedForCompare) <= 6:
            self.controller.selectedForCompare = self.selectedForCompare
            self.controller.show_compare()
        else:
            if len(self.selectedForCompare) > 6:
                msg = "ERROR - Too many teams selected"
            else:
                msg = "ERROR - Too few teams selected"

            errorLabel = tk.Label(self, text=msg, font=global_variables.text(12))
            errorLabel.grid(row=8, column=0)