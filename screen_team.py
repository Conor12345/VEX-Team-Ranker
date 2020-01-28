import tkinter as tk
import global_variables
import team_management
import api_query

class TeamView(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

    def bindSetup(self):
        self.teamNum = self.controller.teamNum
        rowNum = 0

        returnButton = tk.Button(self, text="Return", font=global_variables.text())
        returnButton.grid(row=rowNum, column=0, sticky="W", padx=10, pady=10)
        rowNum += 1

        self.labels = []
        self.labels.append(tk.Label(self, text="Team number: {}".format(self.teamNum), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2)
        rowNum += 1

        self.labels.append(tk.Label(self, text="Team name: {}".format(team_management.get_team_name(self.teamNum)[0:21]), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2)
        rowNum += 1

        self.labels.append(tk.Label(self, text="Team location: {}".format(team_management.get_team_city(self.teamNum)[0:21]), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2)
        rowNum += 1

        self.labels.append(tk.Label(self, text=" ", font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2)
        rowNum += 1

        self.labels.append(tk.Label(self, text="Most recent skill rating: {}".format(round(team_management.get_team_skill(self.teamNum), 3)), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2)
        rowNum += 1

        matchWinRate = None
        if self.controller.teamDict is not None:
            if self.teamNum in self.controller.teamDict:
                winLossDraw = self.controller.teamDict[self.teamNum][1]
                matchWinRate = round((winLossDraw[0] + 0.5 * winLossDraw[2]) / sum(winLossDraw), 3)

        self.labels.append(tk.Label(self, text="Match win rate: {}".format(matchWinRate), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2)
        rowNum += 1

        altSkill = None
        if self.controller.selectedSeason != "":
            altSkill = round(api_query.get_alt_skill(self.teamNum, self.controller.selectedSeason), 3)

        self.labels.append(tk.Label(self, text="Alternate skill rating: {}".format(altSkill), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2)
        rowNum += 1