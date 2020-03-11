import tkinter as tk

import account_management
import pc_identifier
from screen_algorithm import Algorithm
from screen_database import Database
from screen_home import Home
from screen_login import Login
from screen_results import Results
from screen_team import TeamView
from screen_compare import Compare

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(pc_identifier.getRes())
        self.title("Main")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.currentUser = ""
        self.isAdmin = False
        self.teamNum = ""
        self.teamDict = None

        self.buttonStates = [0 for i in range(20)]
        self.teamDisplay = ""

        self.selectedTeams = []
        self.selectedSeason = ""
        self.selectedCountry = ""

        self.frames = {}
        self.currentFrame = Login

        for F in [Login, Home, Database, Algorithm, Results, TeamView, Compare]:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, container):
        self.frames[container].tkraise()
        self.frames[container].bindSetup()

    def login_success(self, UserName):
        self.currentUser = UserName
        self.isAdmin = account_management.is_admin(UserName)
        self.teamNum = account_management.get_user_data(UserName)[3]

    def show_database(self):
        self.currentFrame = Database
        self.show_frame(Database)

    def show_home(self):
        self.currentFrame = Home
        self.show_frame(Home)

    def show_algorithm(self):
        self.currentFrame = Algorithm
        self.show_frame(Algorithm)

    def show_results(self):
        self.currentFrame = Results
        self.show_frame(Results)

    def show_team(self):
        self.show_frame(TeamView)

    def show_compare(self):
        self.currentFrame = Compare
        self.show_frame(Compare)

app = Main()
app.state(pc_identifier.getType())
app.mainloop()