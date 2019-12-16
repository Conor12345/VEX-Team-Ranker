import sqlite3
import tkinter as tk

import event_management
import global_variables
import team_management


class Algorithm(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)


    def bindSetup(self):
        self.season = self.controller.selectedSeason
        self.country = self.controller.selectedCountry
        self.teamsToOutput = self.controller.selectedTeams

        self.currentLabel = tk.Label(self, text="Current task : Fetching complete team list", font=global_variables.text(20))
        self.currentLabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.teamDict = {}
        self.eventNames = event_management.get_event_list(self.country, self.season)
        for eventName in self.eventNames:
            for teamNum in team_management.get_team_list(eventName):
                if teamNum not in self.teamDict:
                    self.teamDict[teamNum] = 50 # TODO make this use existing skill values + pick start value

        db = sqlite3.connect("database.db")
        c = db.cursor()
        results = c.execute("SELECT MatchLevel, RedTeam1, RedTeam2, BlueTeam1, BlueTeam2, RedScore, BlueScore, Date "
                            "FROM tblMatches JOIN tblEvents ON tblMatches.EventID = tblEvents.EventID "
                            "WHERE Country='United Kingdom' AND Season='Turning Point'").fetchall()
        print(results)