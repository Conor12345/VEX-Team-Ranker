import tkinter as tk
from math import ceil

import api_query
import event_management
import global_variables
import team_management


class Compare(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

    def bindSetup(self):
        self.selectedForCompare = [x[1] for x in self.controller.selectedForCompare]  # Store team list locally
        numTeams = len(self.selectedForCompare)
        rowNum = 0  # Row counter to be incremented after use

        returnButton = tk.Button(self, text="Return", font=global_variables.text(), command=self.goBack)
        returnButton.grid(row=0, column=0, sticky="W", padx=10, pady=10, columnspan=100)

        self.spacer = tk.Frame(self, padx=20, pady=20)
        self.spacer.grid(row= 1, column=0, sticky="NESW")

        self.boxes = []  # Generate empty array
        for row1 in range(int(ceil(numTeams / 2))):  # Loop for top row
            self.boxes.append(tk.Frame(self.spacer, padx=20, pady=20, highlightbackground="black", highlightthickness=1))  # Create empty frame
            self.boxes[-1].grid(row=rowNum, column=2 * row1, columnspan=2, sticky="NESW")  # Place empty frame on grid
        rowNum += 1  # Move onto next row

        if numTeams % 2 == 0:  # If num of teams on second row is even
            wid = 2
        else:
            if numTeams == 3:
                wid = 4
            else:
                wid = 3

        for row2 in range(int(numTeams - (numTeams / 2))):  # Loop for bottom row
            self.boxes.append(tk.Frame(self.spacer, padx=20, pady=20, highlightbackground="black", highlightthickness=1))  # Create empty frame
            self.boxes[-1].grid(row=rowNum, column=wid * row2, columnspan=wid, sticky="NESW")  # Place empty frame on grid
        rowNum += 1

        self.data = []
        for teamNum in self.selectedForCompare:
            teamData = [["Team number", teamNum], ["Team name", team_management.get_team_name(teamNum)], ["Team city", team_management.get_team_city(teamNum)],
                        ["Skill rating", round(team_management.get_team_skill(teamNum),2)]]  # Collect simple data from database

            if self.controller.selectedSeason != "":  # Data which requires the season to have been selected
                teamData.append(["Alt skill rating", round(api_query.get_alt_skill(teamNum, self.controller.selectedSeason), 2)])
                teamData.append(["Awards won", api_query.get_num_awards(teamNum, self.controller.selectedSeason)])
                teamData.append(["Average constribution to wins", event_management.get_average_contribution_to_win(teamNum, self.controller.selectedSeason)])

            matchWinRate = None  # Sets none value to be overwritten if needed
            if self.controller.teamDict is not None:  # Checks if algorithm has run
                winLossDraw = self.controller.teamDict[teamNum][1]  # Stores win loss draw numbers locally
                matchWinRate = round((winLossDraw[0] + 0.5 * winLossDraw[2]) / sum(winLossDraw) * 100, 2)  # Calculates match win rate as %
            if matchWinRate is not None:
                teamData.append(["Match win rate", matchWinRate])

            self.data.append(teamData)

        for i in range(3, len(self.data[0])): # Iterate through each ranking factor
            minimum = 110 # Minimum value to be overwritten
            maximum = -110 # Maximum value to be overwritten
            for team in self.data: # Iterate through each team to find min/max
                if team[i][1] < minimum:
                    minimum = team[i][1]
                if team[i][1] > maximum:
                    maximum = team[i][1]

            for team in self.data: # Iterates through each team, calculate the colour values
                team[i].append(int(global_variables.remap(team[i][1], minimum, maximum, 0, 255 * 2)) - 255) # Appends the RGB value

        labels = []
        for boxID in range(len(self.data)):
            rowNum = 0
            for dataItem in self.data[boxID]:
                labels.append(tk.Label(self.boxes[boxID], text=dataItem[0] + ": ", font=global_variables.text(16)))
                labels[-1].grid(row=rowNum, column=0, sticky="NESW")

                if len(dataItem) > 2:
                    hexNum = str(hex(dataItem[2]))[-2:]
                    if hexNum[0] == "x":
                        hexNum = "0" + hexNum[1]

                    if dataItem[2] > 0:
                        col = "#00{}00".format(hexNum)
                    elif dataItem[2]:
                        col = "#{}0000".format(hexNum)
                    else:
                        col = "#000000"
                else:
                    col = "#000000"

                labels.append(tk.Label(self.boxes[boxID], text=dataItem[1], font=global_variables.text(16), foreground=col))
                labels[-1].grid(row=rowNum, column=1, sticky="NESW")

                rowNum += 1

            labels.append(tk.Button(self.boxes[boxID], text="Show team view", font=global_variables.text(16), command=lambda boxID=boxID: self.showTeamView(boxID)))
            labels[-1].grid(row=rowNum, column=1, sticky="NESW")
            rowNum += 1

    def goBack(self):
        for box in self.boxes:
            box.grid_forget()
        self.controller.show_frame(self.controller.currentFrame)

    def showTeamView(self, teamNum):
        print(teamNum, self.data[teamNum][0][1])
        self.controller.teamDisplay = self.data[teamNum][0][1]
        self.controller.show_team()