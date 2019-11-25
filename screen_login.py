import tkinter as tk

import account_management


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
        self.controller.bind("<Return>", self.submitLogin)

    def submitLogin(self, blank=None):
        if self.userBox.get() + self.passBox.get() == "": # Automatic login for testing purposes
            self.userBox.insert(0, "Admin")
            self.passBox.insert(0, "12345")

        if account_management.verify_user_login(self.userBox.get(), self.passBox.get()): # Checks whether the credentials are correct
            self.controller.login_success(self.userBox.get()) # Stores user information
            self.controller.show_home() # Switches to the home screen
        else:
            errorMsg = tk.Label(self, text="ERROR - Login Unsuccessful", font=("Verdana", 18)) # Prints error msg on screen
            errorMsg.place(relx=0.5, rely=0.8, anchor="center")
