import tkinter as tk

import account_management
import global_variables
import pc_identifier


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

        self.frames = {}

        for F in [Login, Home]:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, container):
        self.frames[container].tkraise()

    def login_success(self, UserName):
        self.currentUser = UserName
        self.isAdmin = account_management.is_admin(UserName)
        self.teamNum = account_management.get_user_data(UserName)[3]


class Login(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        titleLabel = tk.Label(self, text="Login", font=("Verdana", 48))
        titleLabel.place(relx=0.5, rely=0.25, anchor="center")

        userLabel = tk.Label(self, text="Username:", font=("Verdana", 20))
        userLabel.place(relx=0.3, rely=0.45, anchor="center")

        self.userBox = tk.Entry(self, width=20, font=("Verdana", 20))
        self.userBox.place(relx=0.5, rely=0.45, anchor="center")

        passLabel = tk.Label(self, text=" Password:", font=("Verdana", 20))
        passLabel.place(relx=0.3, rely=0.55, anchor="center")

        self.passBox = tk.Entry(self, width=20, font=("Verdana", 20), show="*")
        self.passBox.place(relx=0.5, rely=0.55, anchor="center")

        self.submitButton = tk.Button(self, text="Submit", command=self.submitLogin, font=("Verdana", 20))
        self.submitButton.place(relx=0.5, rely=0.7, anchor="center")

        self.userBox.focus()

    def submitLogin(self):
        if self.userBox.get() + self.passBox.get() == "":
            self.userBox.insert(0, "Admin")
            self.passBox.insert(0, "12345")

        if account_management.verify_user_login(self.userBox.get(), self.passBox.get()):
            self.controller.login_success(self.userBox.get())
            self.controller.show_frame(Home)
        else:
            errorMsg = tk.Label(self, text="ERROR - Login Unsuccessful", font=("Verdana", 18))
            errorMsg.place(relx=0.5, rely=0.8, anchor="center")


class Home(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.navbarGrid = tk.Frame(self)
        self.navbarGrid.place(x=20, y=20)

        self.homeButton = tk.Button(self.navbarGrid, text="Home", font=global_variables.text(), padx=20)
        self.homeButton.grid(row=0, column=1)

        self.databaseButton = tk.Button(self.navbarGrid, text="Database", font=global_variables.text())
        self.databaseButton.grid(row=0, column=2)

        self.resultsButton = tk.Button(self.navbarGrid, text="Results", font=global_variables.text())
        self.resultsButton.grid(row=0, column=3)


        self.importEventGrid = tk.Frame(self, width=800, bg="blue")
        self.importEventGrid.place(x=40, y=100)

        importEventLabel = tk.Label(self.importEventGrid, text="Select teams via Event", font=global_variables.text())
        importEventLabel.grid(row=0, column=0, columnspan=2)

        seasonLabel = tk.Label(self.importEventGrid, text="Season:", font=global_variables.text())
        seasonLabel.grid(row=2, column=0)

        self.currentSeasonVar = tk.StringVar(self)
        self.currentSeasonVar.set("Choose season")

        self.seasonMenu = tk.OptionMenu(self.importEventGrid, self.currentSeasonVar, *global_variables.seasons())
        self.seasonMenu.grid(row=2, column=1)

        countryLabel = tk.Label(self.importEventGrid, text="Country:", font=global_variables.text())
        countryLabel.grid(row=3, column=0)

        self.currentCountryVar = tk.StringVar(self)
        self.currentCountryVar.set("Choose country")

        self.countryMenu = tk.OptionMenu(self.importEventGrid, self.currentCountryVar, *global_variables.countries())
        self.countryMenu.grid(row=3, column=1)

        eventLabel = tk.Label(self.importEventGrid, text="Event:", font=global_variables.text())
        eventLabel.grid(row=4, column=0)

        self.currentEventVar = tk.StringVar(self)
        self.currentEventVar.set("Choose event")

        self.eventMenu = tk.OptionMenu(self.importEventGrid, self.currentEventVar, "test1", "test2", "test3")
        self.eventMenu.grid(row=4, column=1)

        self.importEventSubmit = tk.Button(self.importEventGrid, text="Select teams", font=global_variables.text())
        self.importEventSubmit.grid(row=5, column=0, columnspan=2)


        self.importTeamGrid = tk.Frame(self)
        self.importTeamGrid.place(x=40, y=400)

        importTeamLabel = tk.Label(self.importTeamGrid, text="Select team via team number", font=global_variables.text())
        importTeamLabel.grid(row=0, column=0)

        self.importTeamBox = tk.Entry(self.importTeamGrid, font=global_variables.text())
        self.importTeamBox.grid(row=1, column=0)

        importTeamNote = tk.Label(self.importTeamGrid, text="Use commas to separate teams", font=global_variables.text(10))
        importTeamNote.grid(row=2, column=0)

        self.importTeamSubmit = tk.Button(self.importTeamGrid, text="Select teams", font=global_variables.text())
        self.importTeamSubmit.grid(row=3, column=0, columnspan=2)


app = Main()
app.state(pc_identifier.getType())
app.mainloop()
