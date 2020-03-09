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
        self.selectedForCompare = [x[1] for x in self.controller.selectedForCompare] # Store team list locally
        numTeams = len(self.selectedForCompare)
        rowNum = 0 # Row counter to be incremented after use

        returnButton = tk.Button(self, text="Return", font=global_variables.text(), command=self.goBack)
        returnButton.grid(row=rowNum, column=0, sticky="W", padx=10, pady=10, columnspan=100)
        rowNum += 1

        self.boxes = [] # Generate empty array
        for row1 in range(int(ceil(numTeams / 2))): # Loop for top row
            self.boxes.append(tk.Frame(self, padx=5, pady=5)) # Create empty frame
            self.boxes[-1].grid(row=rowNum, column=2*row1, columnspan=2) # Place empty frame on grid
        rowNum += 1 # Move onto next row

        if numTeams % 2 == 0: # If num of teams on second row is even
            wid = 2
        else:
            if numTeams == 3:
                wid = 4
            else:
                wid = 3

        for row2 in range(int(numTeams - (numTeams / 2))): # Loop for bottom row
            self.boxes.append(tk.Frame(self, padx=5, pady=5)) # Create empty frame
            self.boxes[-1].grid(row=rowNum, column=wid*row2, columnspan=wid) # Place empty frame on grid
        rowNum += 1

        self.data = []
        for teamNum in self.selectedForCompare:
            teamData = [["Team number", teamNum], ["Team name", team_management.get_team_name(teamNum)], ["Team city", team_management.get_team_city(teamNum)],
                        ["Skill rating", team_management.get_team_skill(teamNum)]] # Collect simple data from database

            if self.controller.selectedSeason != "": # Data which requires the season to have been selected
                teamData.append(["Alt skill rating", api_query.get_alt_skill(teamNum, self.controller.selectedSeason)])
                teamData.append(["Awards won", api_query.get_num_awards(teamNum, self.controller.selectedSeason)])
                teamData.append(["Average constribution to wins", event_management.get_average_contribution_to_win(teamNum, self.controller.selectedSeason)])

            matchWinRate = None  # Sets none value to be overwritten if needed
            if self.controller.teamDict is not None:  # Checks if algorithm has run
                winLossDraw = self.controller.teamDict[teamNum][1]  # Stores win loss draw numbers locally
                matchWinRate = str(round((winLossDraw[0] + 0.5 * winLossDraw[2]) / sum(winLossDraw), 3) * 100) + "%"  # Calculates match win rate as %
            if matchWinRate is not None:
                teamData.append(["Match win rate", str(matchWinRate)])

    def goBack(self):
        for box in self.boxes:
            box.grid_forget()
        self.controller.show_frame(self.controller.currentFrame)