import tkinter as tk

import event_management
import global_variables
import team_management


class Home(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.navbarGrid = tk.Frame(self, padx=10, pady=10)
        self.navbarGrid.grid(row=0, column=0)

        self.homeButton = tk.Button(self.navbarGrid, text="Home", font=global_variables.text())
        self.homeButton.grid(row=0, column=1)

        self.databaseButton = tk.Button(self.navbarGrid, text="Database", font=global_variables.text(), command=self.controller.show_database)
        self.databaseButton.grid(row=0, column=2)

        self.resultsButton = tk.Button(self.navbarGrid, text="Results", font=global_variables.text())
        self.resultsButton.grid(row=0, column=3)

        self.importEventGrid = tk.Frame(self, padx=10, pady=10)
        self.importEventGrid.grid(row=1, column=0)

        importEventLabel = tk.Label(self.importEventGrid, text="Select teams via Event", font=global_variables.text())
        importEventLabel.grid(row=0, column=0, columnspan=3)

        self.currentSeasonVar = tk.StringVar(self)
        self.currentSeasonVar.set("Choose season")

        self.currentCountryVar = tk.StringVar(self)
        self.currentCountryVar.set("United Kingdom")

        self.currentEventVar = tk.StringVar(self)
        self.currentEventVar.set("Choose event")

        countryLabel = tk.Label(self.importEventGrid, text="Country:", font=global_variables.text(12))
        countryLabel.grid(row=3, column=0)

        self.countryMenu = tk.OptionMenu(self.importEventGrid, self.currentCountryVar, *global_variables.countries())
        self.countryMenu.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        self.countryMenu.config(font=global_variables.text(12))

        eventLabel = tk.Label(self.importEventGrid, text="Event:", font=global_variables.text(12))
        eventLabel.grid(row=4, column=0)

        self.eventMenu = tk.OptionMenu(self.importEventGrid, self.currentEventVar, "Select country and season")
        self.eventMenu.grid(row=4, column=1, columnspan=2, padx=10, pady=10)
        self.eventMenu.config(font=global_variables.text(12))

        seasonLabel = tk.Label(self.importEventGrid, text="Season:", font=global_variables.text(12))
        seasonLabel.grid(row=2, column=0)

        self.seasonMenu = tk.OptionMenu(self.importEventGrid, self.currentSeasonVar, *tuple(global_variables.seasons()), command=self.updateEventMenu)
        self.seasonMenu.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        self.seasonMenu.config(font=global_variables.text(12))

        self.importEventSubmit = tk.Button(self.importEventGrid, text="Select teams", font=global_variables.text(16), command=self.importTeamsByEvent)
        self.importEventSubmit.grid(row=5, column=0, columnspan=2)

        self.importTeamGrid = tk.Frame(self, padx=10, pady=10)
        self.importTeamGrid.grid(row=2, column=0)

        importTeamLabel = tk.Label(self.importTeamGrid, text="Select team via team number", font=global_variables.text())
        importTeamLabel.grid(row=0, column=0)

        self.importTeamBox = tk.Entry(self.importTeamGrid, font=global_variables.text(12))
        self.importTeamBox.grid(row=1, column=0)

        importTeamNote = tk.Label(self.importTeamGrid, text="Use commas to separate teams", font=global_variables.text(10))
        importTeamNote.grid(row=2, column=0)

        self.importTeamSubmit = tk.Button(self.importTeamGrid, text="Select teams", font=global_variables.text(16), command=self.importTeamsByTeamNum)
        self.importTeamSubmit.grid(row=3, column=0)

        self.dataGrid = tk.Frame(self, padx=10, pady=10)
        self.dataGrid.grid(row=1, column=1, rowspan=2)

        selectedTeamsLabel = tk.Label(self.dataGrid, text="Currently selected teams:", font=global_variables.text())
        selectedTeamsLabel.grid(row=0, column=0, columnspan=2)

        self.dataListbox = tk.Listbox(self.dataGrid, width=10, height=16)
        self.dataListbox.grid(row=2, column=0, rowspan=7)
        self.dataListbox.config(font=global_variables.text(16))

        self.removeTeamButton = tk.Button(self.dataGrid, text="Remove selected team", font=global_variables.text(16), command=self.removeTeam)
        self.removeTeamButton.grid(row=2, column=1)

        self.removeAllTeamsButton = tk.Button(self.dataGrid, text="Remove allteams", font=global_variables.text(16), command=self.removeAllTeams)
        self.removeAllTeamsButton.grid(row=3, column=1)

        self.viewTeamDataButton = tk.Button(self.dataGrid, text="View selected team", font=global_variables.text(16))
        self.viewTeamDataButton.grid(row=4, column=1)

        for record in range(0, len(self.controller.selectedTeams)):
            row = self.controller.selectedTeams[record]
            self.dataListbox.insert(tk.END, row)

        self.finalSeasonVar = tk.StringVar(self)
        self.finalSeasonVar.set("Choose season")

        self.finalCountryVar = tk.StringVar(self)
        self.finalCountryVar.set("United Kingdom")

        finalCountryLabel = tk.Label(self.dataGrid, text="Country:", font=global_variables.text(12))
        finalCountryLabel.grid(row=5, column=1)

        self.finalCountryMenu = tk.OptionMenu(self.dataGrid, self.finalCountryVar, *global_variables.countries())
        self.finalCountryMenu.grid(row=6, column=1)
        self.finalCountryMenu.config(font=global_variables.text(12))

        finalseasonLabel = tk.Label(self.dataGrid, text="Season:", font=global_variables.text(12))
        finalseasonLabel.grid(row=7, column=1)

        self.finalSeasonMenu = tk.OptionMenu(self.dataGrid, self.finalSeasonVar, *tuple(global_variables.seasons()), command=self.updateEventMenu)
        self.finalSeasonMenu.grid(row=8, column=1)
        self.finalSeasonMenu.config(font=global_variables.text(12))

        self.beginButton = tk.Button(self.dataGrid, text="Begin analysis", font=global_variables.text())
        self.beginButton.grid(row=9, column=0, columnspan=3)

    def updateEventMenu(self, test):
        if self.currentSeasonVar.get() != "Country:":
            data = event_management.get_event_list(self.currentCountryVar.get(), self.currentSeasonVar.get())
            self.eventMenu["menu"].delete(0, "end")
            for eventName in data:
                self.eventMenu["menu"].add_command(label=eventName, command=tk._setit(self.currentEventVar, eventName))

    def importTeamsByEvent(self, test=None):
        self.controller.selectedTeams += team_management.get_team_list(self.currentEventVar.get())
        self.controller.selectedTeams = sorted(list(set(self.controller.selectedTeams)))
        self.refreshTeamList()

    def refreshTeamList(self, test=None):
        self.dataListbox.delete(0, tk.END)
        if len(self.controller.selectedTeams) > 0:
            for record in range(0, len(self.controller.selectedTeams)):
                row = self.controller.selectedTeams[record]
                self.dataListbox.insert(tk.END, row)

    def removeTeam(self, test=None):
        if len(self.controller.selectedTeams) > 0:
            self.controller.selectedTeams.remove(self.dataListbox.get(tk.ACTIVE))
            self.controller.selectedTeams = sorted(list(set(self.controller.selectedTeams)))
            self.refreshTeamList()

    def importTeamsByTeamNum(self, test=None):
        data = self.importTeamBox.get().replace(" ", "").split(",")
        if len(data) > 0:
            errors = []
            for teamNum in data:
                if team_management.check_team_presence(teamNum):
                    self.controller.selectedTeams.append(teamNum)
                    self.controller.selectedTeams = sorted(list(set(self.controller.selectedTeams)))
                    self.refreshTeamList()
                else:
                    if not team_management.import_team(teamNum):
                        errors.append(teamNum)
            if len(errors) > 0:
                errorLabel = tk.Label(self.importTeamGrid, text="Teams not found: " + "".join(errors), font=global_variables.text(12))
                errorLabel.grid(row=4, column=0)

    def removeAllTeams(self):
        self.controller.selectedTeams = []
        self.refreshTeamList()