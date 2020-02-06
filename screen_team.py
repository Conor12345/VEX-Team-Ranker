import tkinter as tk
import sqlite3
import global_variables
import team_management
import event_management
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

        self.labels.append(tk.Label(self, text="Most recent skill rating: {}".format(round(team_management.get_team_skill(self.teamNum), 2)), font=global_variables.text(20)))
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2, padx=10)
        rowNum += 1

        matchWinRate = None # Sets none value to be overwritten if needed
        if self.controller.teamDict is not None: # Checks if algorithm has run
            if self.teamNum in self.controller.teamDict: # Checks whether selected team was included in comparision
                winLossDraw = self.controller.teamDict[self.teamNum][1] # Stores win loss draw numbers locally
                matchWinRate = str(round((winLossDraw[0] + 0.5 * winLossDraw[2]) / sum(winLossDraw), 3) * 100) + "%" # Calculates match win rate as %

        self.labels.append(tk.Label(self, text="Match win rate: {}".format(matchWinRate), font=global_variables.text(20))) # Creates label
        self.labels[-1].grid(row=rowNum, column=0, columnspan=2) # Places label
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
        self.updateAwardData()

    def updateBox(self, dataBox, data):
        colWidth = int(dataBox["width"] / len(data[0]))
        
        dataBox.delete(0, tk.END)  # Clears databox
        row = ""
        for header in data[0]:  # Adds headers to table
            row += str(header).ljust(colWidth, " ")
        dataBox.insert(tk.END, row)  # Inserts header row
        dataBox.insert(tk.END, " ")  # Inserts empty row for spacing

        for result in data[1:]:
            row = ""
            for record in result:  # Iterates though each column
                if len(str(record)) <= colWidth:  # If the data fits in the space without wrapping
                    row += str(record).ljust(colWidth, " ")  # Adds record with padding on right to fill space
                else:
                    row += str(record)[:colWidth - 1].ljust(colWidth, " ")
            dataBox.insert(tk.END, row)  # Inserts row into table

    def goBack(self):
        for label in self.labels:
            label.grid_forget()
        self.controller.show_frame(self.controller.currentFrame)

    def updateAwardData(self):
        # Awaard Name, Competition Name, Season, Date
        data = [["Award", "Competition Name", "Season", "Date"]]

        results = api_query.get_awards("1591B")
        for result in results:
            eventData = event_management.get_event_data(result["sku"])
            data.append([result["name"], eventData[1], eventData[4], eventData[5]])

        self.updateBox(self.awardBox, data)

    def updateTournamentData(self):
        # Competition Name, Location, Data, Season, Qualifying Ranking, W-L-T, Autonomous Points, Max score, Contribution to Wins
        data = [["EventName", "City", "Date", "Season", "Qualifying Ranking", "W-L-T", "Autonomous Points", "Max score", "Contribution to wins"]]
        db = sqlite3.connect("database.db")
        c = db.cursor()
        results = c.execute("SELECT DISTINCT tM.EventID, EventName, City, Date, Season "
                            "FROM tblEvents INNER JOIN tblMatches tM on tblEvents.EventID = tM.EventID "
                            "WHERE (RedTeam1 =(?) OR RedTeam2 = (?) OR BlueTeam1 = (?) OR BlueTeam2 = (?)) "
                            "ORDER BY Date DESC", (self.teamNum, self.teamNum, self.teamNum, self.teamNum)).fetchall()

        for result in results:
            additionalData = api_query.get_event_results(result[0], self.teamNum)
            data.append(list(result[1:]) +
                        [additionalData["rank"], "{}-{}-{}".format(additionalData["wins"], additionalData["losses"], additionalData["ties"])
                            , additionalData["ap"], additionalData["max_score"], additionalData["ccwm"]])

        self.updateBox(self.tournamentBox, data)