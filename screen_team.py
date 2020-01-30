import tkinter as tk
import sqlite3
import global_variables
import team_management
import api_query

class TeamView(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

    def bindSetup(self):
        self.teamNum = self.controller.teamDisplay
        rowNum = 0

        returnButton = tk.Button(self, text="Return", font=global_variables.text(), command=self.goBack)
        returnButton.grid(row=rowNum, column=0, sticky="W", padx=10, pady=10)
        rowNum += 1

        self.labels = []
        self.labels.append(tk.Label(self, text="Team number: {}".format(self.teamNum), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2, padx=10)
        rowNum += 1

        self.labels.append(tk.Label(self, text="Team name: {}".format(team_management.get_team_name(self.teamNum)[0:21]), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2, padx=10)
        rowNum += 1

        data = team_management.get_team_city(self.teamNum)[0:21]
        if data == "":
            data = None
        self.labels.append(tk.Label(self, text="Team location: {}".format(data), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2, padx=10)
        rowNum += 1

        self.labels.append(tk.Label(self, text=" ", font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2, padx=10)
        rowNum += 1

        self.labels.append(tk.Label(self, text="Most recent skill rating: {}".format(round(team_management.get_team_skill(self.teamNum), 3)), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2, padx=10)
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

        rowNum += 1
        self.labels.append(tk.Label(self, text="Tournament History", font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=3)
        rowNum += 1

        self.tournamentBox = tk.Listbox(self, width=185, height=20)
        self.tournamentBox.grid(row=rowNum + 1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.tournamentBox.config(font=("Courier", 12))

        self.labels.append(tk.Label(self, text="Award History", font=global_variables.text(20)))
        self.labels[-1].grid(row=1, column=2, columnspan=1)

        self.awardBox = tk.Listbox(self, width=135, height=20)
        self.awardBox.grid(row=2, column=2, rowspan=7, padx=10, pady=10, sticky="ew")
        self.awardBox.config(font=("Courier", 12))

        self.updateTournamentData()

    def updateBox(self, dataBox, data):
        pass

    def goBack(self):
        for label in self.labels:
            label.grid_forget()
        self.controller.show_frame(self.controller.currentFrame)

    def updateAwardData(self):
        pass

    def updateTournamentData(self):
        # Competition Name, Location, Data, Season, Qualifying Ranking, W-L-T, Autonomous Points, Max score, Contribution to Wins
        columnHeads = ["EventName", "City", "Date", "Season"]
        db = sqlite3.connect("database.db")
        c = db.cursor()
        results = columnHeads + c.execute('SELECT EventName, City, Date, Season FROM tblEvents WHERE '
                            '((RedTeam1 LIKE (?) OR RedTeam2 LIKE (?) OR BlueTeam1 LIKE (?) OR BlueTeam2 LIKE (?)))',
                            (self.teamNum, self.teamNum, self.teamNum, self.teamNum)).fetchall()

        print(results)

        self.updateBox(self.tournamentBox, results)