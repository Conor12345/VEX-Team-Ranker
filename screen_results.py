import tkinter as tk

import api_query
import global_variables
import team_management


def get5thElement(array):
    return array[4]


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

        self.descriptionLabel = tk.Label(self, text="Select teams to compare", font=global_variables.text())
        self.descriptionLabel.grid(row=1, column=0, padx=10)

        self.showTeamButton = tk.Button(self, text="Show highlighted team details", font=global_variables.text(14))
        self.showTeamButton.grid(row=2, column=0)

        self.compareSelectedButton = tk.Button(self, text="Compare selected teams", font=global_variables.text(14))
        self.compareSelectedButton.grid(row=3, column=0)

        self.fetchAwardDataButton = tk.Button(self, text="Collect award data", font=global_variables.text(14), command=self.fetchAwardData)
        self.fetchAwardDataButton.grid(row=4, column=0)

        self.dataBox = tk.Listbox(self, width=140, height=42)
        self.dataBox.grid(row=1, column=2, rowspan=20)
        self.dataBox.config(font=("Courier", 12))

        self.tickBoxGrid = tk.Frame(self)
        self.tickBoxGrid.grid(row=1, column=1, rowspan=20, padx=10)

        selectLabel = tk.Label(self.tickBoxGrid, text="Selected?", font=global_variables.text(12))
        selectLabel.grid(row=0, column=0)

        self.tickBoxData = []
        self.tickBoxes = []
        for i in range(20):
            self.tickBoxData.append(tk.IntVar())
            self.tickBoxes.append(tk.Checkbutton(self.tickBoxGrid, variable=self.tickBoxData[i]))
            self.tickBoxes[-1].grid(row=i + 1, column=0, pady=7)

        self.upButton = tk.Button(self, text="/\\", command=self.moveUp)
        self.upButton.grid(row=0, column=2)

        self.downButton = tk.Button(self, text="\\/",command=self.moveDown)
        self.downButton.grid(row=30, column=2, pady=10)

    def bindSetup(self):
        self.currentScreen = 0
        self.updateData()

    def updateData(self):
        # Rank, Team Num, Team Name, Team City, Skill rating, Match win rate, Total awards

        self.display = []
        for team in self.controller.selectedTeams + [self.controller.teamNum]:
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

        for result in self.display[self.currentScreen * 20 : (self.currentScreen + 1) * 20]:  # Iterates through each record
            rows = [""]
            for record in result:  # Iterates though each column
                if len(str(record)) <= self.columnWidth:  # If the data fits in the space without wrapping
                    rows[0] += str(record).ljust(self.columnWidth, " ")  # Adds record with padding on right to fill space
                else:
                    rows[0] += str(record)[:19].ljust(self.columnWidth, " ")
            for row in rows:  # Iterates through each row in cage
                self.dataBox.insert(tk.END, row)  # Inserts row into table
                self.dataBox.insert(tk.END, " ")

    def moveDown(self):
        if self.currentScreen < (len(self.display) / 20) - 1:
            self.currentScreen += 1
            self.updateScreen()

    def moveUp(self):
        if self.currentScreen != 0:
            self.currentScreen -= 1
            self.updateScreen()

    def fetchAwardData(self):
        for row in self.display:
            if self.controller.selectedSeason != "":
                row[6] = api_query.get_num_awards(row[1], self.controller.selectedSeason)
        self.updateScreen()

