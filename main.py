import tkinter as tk

import account_management
import pc_identifier
from screen_algorithm import Algorithm
from screen_database import Database
from screen_home import Home
from screen_login import Login
from screen_results import Results


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

        self.selectedTeams = []
        self.selectedSeason = ""
        self.selectedCountry = ""

        self.frames = {}

        for F in [Login, Home, Database, Algorithm, Results]:
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
        self.show_frame(Database)

    def show_home(self):
        self.show_frame(Home)

    def show_algorithm(self):
        self.show_frame(Algorithm)

    def show_results(self):
        self.show_frame(Results)

app = Main()
app.state(pc_identifier.getType())
app.mainloop()