import tkinter as tk
import account_management
import pc_identifier
import globalVars

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

        titleLabel = tk.Label(self, text="Login", font=globalVars.text(48))
        titleLabel.grid(row=0, column=1, columnspan=4)

        userLabel = tk.Label(self, text="Username:", font=globalVars.text())
        userLabel.grid(row=2, column=2)

        self.userBox = tk.Entry(self, width=20, font=globalVars.text())
        self.userBox.grid(row=2, column= 4)

        passLabel = tk.Label(self, text=" Password:", font=globalVars.text())
        passLabel.grid(row=3, column=2)

        self.passBox = tk.Entry(self, width=20, font=globalVars.text(), show="*")
        self.passBox.grid(row=3, column=4)

        self.submitButton = tk.Button(self, text="Submit", command=self.submitLogin, font=globalVars.text())
        self.submitButton.grid(row=5, column=1, columnspan=4)

        self.userBox.focus()

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(5, weight=2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

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

        self.leftGrid = tk.Frame(self)
        self.leftGrid.grid(row=2, column=0, columnspan=5)

        self.homeButton = tk.Button(self, text="Home", font=globalVars.text())
        self.homeButton.grid(row=0, column=1)

        self.databaseButton = tk.Button(self, text="Database", font=globalVars.text())
        self.databaseButton.grid(row=0, column=2)

        self.resultsButton = tk.Button(self, text="Results", font=globalVars.text())
        self.resultsButton.grid(row=0, column=3)

        importEventLabel = tk.Label(self.leftGrid, text="Import team via Event", font=globalVars.text())
        importEventLabel.grid(row=0, column=0, columnspan=2)

        eventLabel = tk.Label(self.leftGrid, text="Season:", font=globalVars.text())
        eventLabel.grid(row=1, column= 0)

        self.currentEventVar = tk.StringVar(self)
        self.currentEventVar.set(globalVars.seasons()[-1])


        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

app = Main()
app.state(pc_identifier.getType())
app.mainloop()
