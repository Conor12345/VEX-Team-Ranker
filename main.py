import tkinter as tk
import account_management

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1280x720+-1600+100")
        self.title("Main")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [Login, Home]:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class Login(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        titleLabel = tk.Label(self, text="Login", font=("Verdana", 48))
        titleLabel.place(relx=0.5, rely=0.25, anchor="center")

        userLabel = tk.Label(self, text="Username:", font=("Verdana", 24))
        userLabel.place(relx=0.2, rely=0.45, anchor="center")

        self.userBox = tk.Entry(self, width=20, font=("Verdana", 24))
        self.userBox.place(relx=0.5, rely=0.45, anchor="center")

        passLabel = tk.Label(self, text="Password:", font=("Verdanaet", 24))
        passLabel.place(relx=0.2, rely=0.55, anchor="center")

        self.passBox = tk.Entry(self, width=20, font=("Verdana", 24), show="*")
        self.passBox.place(relx=0.5, rely=0.55, anchor="center")

        self.submitButton = tk.Button(self, text="Submit", command=self.submitLogin, font=("Verdana", 24))
        self.submitButton.place(relx=0.5, rely=0.7, anchor="center")

        self.userBox.focus()

    def submitLogin(self):
        if account_management.verify_user_login(self.userBox.get(), self.passBox.get()):
            print("login sucess")
        else:
            errorMsg = tk.Label(self, text="ERROR - Login Unsuccessful", font=("Verdana", 18))
            errorMsg.place(relx=0.5, rely=0.8, anchor="center")

class Home(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

app = Main()
app.mainloop()