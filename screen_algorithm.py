import sqlite3
import tkinter as tk
from math import ceil

from numpy import tan, arctan
from scipy.odr import *

import event_management
import global_variables
import team_management

timeDelay = 1000


def normaliseFunction(Coefs, X):
    return Coefs[0] + Coefs[1] * tan(Coefs[2] * X)


def inverseF(Coefs, X):
    return (1 / Coefs[2]) * arctan((X - Coefs[0]) / Coefs[1])


class Algorithm(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

    def bindSetup(self):
        self.cyclesCompletedCount = 0

        self.currentLabel = tk.Label(self, text="Current task : Fetching complete team list", font=global_variables.text(20))
        self.currentLabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.controller.after(timeDelay, self.dataSetup)

    def dataSetup(self):
        self.season = self.controller.selectedSeason
        self.country = self.controller.selectedCountry
        self.teamsToOutput = self.controller.selectedTeams

        self.teamDict = {}
        self.eventNames = event_management.get_event_list(self.country, self.season)
        for eventName in self.eventNames:
            for teamNum in team_management.get_team_list(eventName):
                if teamNum not in self.teamDict:
                    self.teamDict[teamNum] = [team_management.get_team_skill(teamNum), [0,0,0]] # [Skill, [W, L, D]]

        db = sqlite3.connect("database.db")
        c = db.cursor()
        self.results = c.execute("SELECT MatchLevel, RedTeam1, RedTeam2, BlueTeam1, BlueTeam2, RedScore, BlueScore, Season "
                                 "FROM tblMatches JOIN tblEvents ON tblMatches.EventID = tblEvents.EventID "
                                 "WHERE Country=(?) AND Season=(?)", (self.country, self.season)).fetchall()

        self.currentLabel.config(text="Current task : Ranking teams - Cycle 1")

        self.controller.after(timeDelay, self.mainAlgorithm)

    def mainAlgorithm(self):
        # MatchLevel 0, RedTeam1 1, RedTeam2 2, BlueTeam1 3, BlueTeam2 4, RedScore 5, BlueScore 6, Season 7
        # (2, '10173S', '10173X', '1408G', '33434A', 12, 16, '2019-03-01')

        for match in self.results:
            teams = match[1:5]
            roundNum = match[0]
            score = match[5:7]
            season = match[7]

            skillRating = []
            for team in teams:
                skillRating.append(self.teamDict[team][0])

            if skillRating[0] == skillRating[1] == skillRating[2] == skillRating[3]:
                probabilities = [0.5, 0.5]
            else:
                print(skillRating)
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
                for team in teams:
                    self.teamDict[team][1][2] += 1

            elif score[0] > score[1]:
                scoreChanges = [1, -1]
                actualWinner = "Red"
                for redTeams in teams[0:2]:
                    self.teamDict[redTeams][1][0] += 1
                for blueTeams in teams[2:4]:
                    self.teamDict[blueTeams][1][1] += 1

            else:
                scoreChanges = [-1, 1]
                actualWinner = "Blue"
                for redTeams in teams[0:2]:
                    self.teamDict[redTeams][1][1] += 1
                for blueTeams in teams[2:4]:
                    self.teamDict[blueTeams][1][0] += 1

            if expectedWinner != actualWinner and actualWinner != "Draw" and expectedWinner != "Draw":
                if probabilities[0] != 0:
                    probabilities[0] = 1 / probabilities[0]
                if probabilities[1] != 0:
                    probabilities[1] = 1 / probabilities[1]

            scoreChanges[0] = scoreChanges[0] * probabilities[0] * roundNum
            scoreChanges[1] = scoreChanges[1] * probabilities[1] * roundNum

            self.teamDict[teams[0]][0] += scoreChanges[0]
            self.teamDict[teams[1]][0] += scoreChanges[0]
            self.teamDict[teams[2]][0] += scoreChanges[1]
            self.teamDict[teams[3]][0] += scoreChanges[1]

        self.cyclesCompletedCount += 1

        if self.cyclesCompletedCount == 10:
            self.currentLabel.config(text="Current task : Outputing results")
            self.controller.after(timeDelay, self.output)

        else:
            self.currentLabel.config(text="Current task : Ranking teams - Cycle {}".format(self.cyclesCompletedCount + 1))
            self.controller.after(timeDelay, self.mainAlgorithm)

    def output(self):
        calculatedSkill = []
        for teamNum in self.teamDict:
            calculatedSkill.append(self.teamDict[teamNum][0])

        model = Model(normaliseFunction)
        x = [j + 1 for j in range(len(calculatedSkill))]

        mydata = RealData(x, sorted(calculatedSkill))
        myodr = ODR(mydata, model, beta0=[10., 100., 0.001])

        myoutput = myodr.run()
        values = myoutput.beta

        minMax = [50, 50]
        for team in self.teamDict:
            normalisedValue = inverseF(values, self.teamDict[team][0])
            if normalisedValue < minMax[0]:
                minMax[0] = normalisedValue
            elif normalisedValue > minMax[1]:
                minMax[1] = normalisedValue
            self.teamDict[team][0] = normalisedValue

        for team in self.teamDict:
            self.teamDict[team][0] = global_variables.remap(self.teamDict[team][0], minMax[0], minMax[1], 0, 100)

        for team in self.teamDict:
            team_management.update_team_skill(team, float(self.teamDict[team][0]))

        self.controller.teamDict = self.teamDict.copy()

        self.controller.buttonStates = [0 for i in range(ceil(len(set(self.controller.selectedTeams + [self.controller.teamNum])) / 20) * 20)]
        self.controller.show_results()
