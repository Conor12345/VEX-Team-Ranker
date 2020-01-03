import sqlite3
import time
import tkinter as tk

import matplotlib.pyplot as plt
import xlwt

import event_management
import global_variables
import team_management


class Algorithm(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

    def bindSetup(self):
        self.currentLabel = tk.Label(self, text="Current task : Fetching complete team list", font=global_variables.text(20))
        self.currentLabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.controller.after(500, self.dataSetup)

    def dataSetup(self):
        self.season = self.controller.selectedSeason
        self.country = self.controller.selectedCountry
        self.teamsToOutput = self.controller.selectedTeams

        self.teamDict = {}
        self.eventNames = event_management.get_event_list(self.country, self.season)
        for eventName in self.eventNames:
            for teamNum in team_management.get_team_list(eventName):
                if teamNum not in self.teamDict:
                    self.teamDict[teamNum] = team_management.get_team_skill(teamNum)

        db = sqlite3.connect("database.db")
        c = db.cursor()
        self.results = c.execute("SELECT MatchLevel, RedTeam1, RedTeam2, BlueTeam1, BlueTeam2, RedScore, BlueScore, Season "
                            "FROM tblMatches JOIN tblEvents ON tblMatches.EventID = tblEvents.EventID "
                            "WHERE Country=(?) AND Season=(?)", (self.country, self.season)).fetchall()

        self.VEXDBSkills = []
        i = 1
        for team in self.teamDict:
            # response = requests.get("https://api.vexdb.io/v1/" + "get_season_rankings" + "?team=" + team)
            # todos = json.loads(response.text)  # load results in JSON, python friendly format
            # VEXDBSkills.append(todos["result"][0]["vrating"])
            self.VEXDBSkills.append(i)
            i += 1

        self.currentLabel = tk.Label(self, text="              Current task : Ranking teams             ", font=global_variables.text(20))
        self.currentLabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.controller.after(500, self.mainAlgorithm)

    def mainAlgorithm(self):
        # MatchLevel 0, RedTeam1 1, RedTeam2 2, BlueTeam1 3, BlueTeam2 4, RedScore 5, BlueScore 6, Season 7
        # (2, '10173S', '10173X', '1408G', '33434A', 12, 16, '2019-03-01')
        for i in range(0, 11):
            for match in self.results:
                teams = match[1:5]
                roundNum = match[0]
                score = match[5:7]
                season = match[7]

                skillRating = []
                for team in teams:
                    skillRating.append(self.teamDict[team])

                probabilities = [(skillRating[0] + skillRating[1]) / sum(skillRating), (skillRating[2] + skillRating[3]) / sum(skillRating)]

                if probabilities[0] == probabilities[1]:
                    expectedWinner = "Draw"
                elif probabilities[0] > probabilities[1]:
                    expectedWinner = "Red"
                else:
                    expectedWinner = "Blue"

                if score[0] == score[1]:
                    scoreChanges = [0.5, 0.5]
                    actualWinner = "Draw"
                elif score[0] > score[1]:
                    scoreChanges = [1, -1]
                    actualWinner = "Red"
                else:
                    scoreChanges = [-1, 1]
                    actualWinner = "Blue"

                if expectedWinner != actualWinner and actualWinner != "Draw" and expectedWinner != "Draw":
                    probabilities[0] = 1 / probabilities[0]
                    probabilities[1] = 1 / probabilities[1]

                scoreChanges[0] = scoreChanges[0] * probabilities[0] * roundNum
                scoreChanges[1] = scoreChanges[1] * probabilities[1] * roundNum

                self.teamDict[teams[0]] += scoreChanges[0]
                self.teamDict[teams[1]] += scoreChanges[0]
                self.teamDict[teams[2]] += scoreChanges[1]
                self.teamDict[teams[3]] += scoreChanges[1]

        calculatedSkill = []
        for teamNum in self.teamDict:
            calculatedSkill.append(self.teamDict[teamNum])

        plt.plot(self.VEXDBSkills, sorted(calculatedSkill), "ro")
        plt.ylabel("Calculated skill values")

        plt.show()

        book = xlwt.Workbook()  # initiate sheet
        sheet = book.add_sheet('Sheet 1')  # create a blank sheet

        sheet.write(1, 1, "VexDBSkill")
        sheet.write(1, 2, "Calculated Skill")

        for i in range(len(calculatedSkill)):
            sheet.write(i + 2, 1, self.VEXDBSkills[i])
            sheet.write(i + 2, 2, calculatedSkill[i])

        book.save('Sample.xls')  # save the sheet to a file
