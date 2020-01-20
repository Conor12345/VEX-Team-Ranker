import sqlite3
import tkinter as tk
from math import ceil

import account_management
import team_management
import event_management
import global_variables
import pc_identifier
import screen_users


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

        self.mainScreenGrid = tk.Frame(self)
        self.mainScreenGrid.grid(row=2, column=0, columnspan=4)

        self.descriptionLabel = tk.Label(self.mainScreenGrid, text="Select teams to compare", font=global_variables.text())
        self.descriptionLabel.grid(row=1, column=0)

        self.showTeamButton = tk.Button(self.mainScreenGrid, text="Show highlighted team details", font=global_variables.text(14))
        self.showTeamButton.grid(row=2, column=0)

        self.compareSelectedButton = tk.Button(self.mainScreenGrid, text="Compare selected teams", font=global_variables.text(14))
        self.compareSelectedButton.grid(row=3, column=0)

        self.dataBox = tk.Listbox(self.mainScreenGrid, width=140, height=42)
        self.dataBox.grid(row=1, column=1, rowspan=8)
        self.dataBox.config(font=("Courier", 12))


    def bindSetup(self):
        self.updateData()

    def updateData(self):
        # Rank, Team Num, Team Name, Team City, Skill rating, Match win rate, Total awards

        self.display = []
        for team in self.controller.selectedTeams:
            tempArray = [None for x in range(7)]

            tempArray[1] = team
            tempArray[2] = team_management.get_team_name(team)
            tempArray[3] = team_management.get_team_city(team)
            tempArray[4] = team_management.get_team_skill(team)

            self.display.append(tempArray)

        self.updateScreen()

    def updateScreen(self):
        self.columnWidth = 20

        self.dataBox.delete(0, tk.END)  # Clears databox
        row = ""
        for header in ["Rank", "Team Number", "Team Name", "City", "Skill rating", "Match win rate", "Total awards won"]:  # Adds headers to table
            row += str(header).ljust(self.columnWidth, " ")
        self.dataBox.insert(tk.END, row)  # Inserts header row
        self.dataBox.insert(tk.END, " ")  # Inserts empty row for spacing

        for result in self.display + [self.controller.teamNum]:  # Iterates through each record
            rows = [""]
            for record in result:  # Iterates though each column
                if len(str(record)) <= self.columnWidth:  # If the data fits in the space without wrapping
                    rows[0] += str(record).ljust(self.columnWidth, " ")  # Adds record with padding on right to fill space
                else:
                    rows[0] += str(record)[:20].ljust(self.columnWidth, " ")

            for row in rows:  # Iterates through each row in cage
                self.dataBox.insert(tk.END, row)  # Inserts row into table
                self.dataBox.insert(tk.END, " ")
