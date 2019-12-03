import tkinter as tk

import account_management
import global_variables
import team_management


class NewUser(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        nameLabel = tk.Label(self, text="New user", font=global_variables.text(16))
        nameLabel.grid(row=0, column=0, columnspan=2)

        self.entryBoxes = []
        labels = ["Username", "Password", "Repeated Password", "Team Number", "Admin"]

        for i in range(5):
            array = [tk.Label(self, text=labels[i], font=global_variables.text(12))]
            array[0].grid(row=i + 1, column=0)

            if i == 4:
                self.AdminVar = tk.IntVar()
                array.append(tk.Checkbutton(self, variable=self.AdminVar))
                array[-1].grid(row=i + 1, column=1)

            elif i == 1 or i == 2:
                array.append(tk.Entry(self, font=global_variables.text(12), show="*"))
                array[-1].grid(row=i + 1, column=1)

            else:
                array.append(tk.Entry(self, font=global_variables.text(12)))
                array[-1].grid(row=i + 1, column=1)

            self.entryBoxes.append(array)

        self.buttons = [tk.Button(self, text="Create User", font=global_variables.text(16), command=self.newUserCreate)]
        self.buttons[0].grid(row=6, column=0, columnspan=2)
        
    def newUserCreate(self):
        if self.entryBoxes[1][1].get() != self.entryBoxes[2][1].get():
            errorLabel = tk.Label(self, text="ERROR - Passwords do not match", font=global_variables.text(12))
            errorLabel.grid(row=7, column=0, columnspan=2)

        elif len(self.entryBoxes[1][1].get()) < 8:
            errorLabel = tk.Label(self, text="ERROR - Passwords must be atleast 8 characters", font=global_variables.text(12))
            errorLabel.grid(row=7, column=0, columnspan=2)

        elif account_management.create_user(self.entryBoxes[0][1].get(), self.entryBoxes[1][1].get(), self.entryBoxes[3][1].get(), self.AdminVar.get()):
            self.parent.show_users()

        else:
            errorLabel = tk.Label(self, text="ERROR - Account creation failed", font=global_variables.text(12))
            errorLabel.grid(row=7, column=0, columnspan=2)

class UpdateUser(NewUser):
    def __init__(self, parent, UserName):
        NewUser.__init__(self, parent)

        nameLabel = tk.Label(self, text="Update user", font=global_variables.text(16))
        nameLabel.grid(row=0, column=0, columnspan=2)

        self.originalUserData = account_management.get_user_data(UserName) # Gets the select users account info
        self.originalUserData[2] = "" # Clears the password location

        self.entryBoxes[0][1].insert(0, self.originalUserData[1]) # Inserts data into the entry boxes
        self.entryBoxes[3][1].insert(0, self.originalUserData[3])

        for button in self.buttons: # Removes buttons from new user init
            button.grid_forget()

        self.buttons = [tk.Button(self, text="Update User", font=global_variables.text(16), command=self.updateUserCommand)]
        self.buttons[0].grid(row=6, column=0, columnspan=2)

        self.buttons.append(tk.Button(self, text="Delete User", font=global_variables.text(16), command=self.deleteUserCommand))
        self.buttons[1].grid(row=7, column=0, columnspan=2)

        if self.originalUserData[4] == 1: # If the user began as an admin
            self.entryBoxes[4][1].select() # Put tick in entry box

    def updateUserCommand(self):
        data = [None for i in range(3)]

        if self.entryBoxes[0][1].get() != self.originalUserData[1]:
            data[0] = self.entryBoxes[0][1].get()

        if self.entryBoxes[3][1].get() != self.originalUserData[3]:
            if not team_management.check_team_presence(self.entryBoxes[3][1].get()):
                if not team_management.import_team(self.entryBoxes[3][1].get()):
                    errorLabel = tk.Label(self, text="ERROR - Team does not exist", font=global_variables.text(12))
                    errorLabel.grid(row=8, column=0, columnspan=2)
                    return False
            data[1] = self.entryBoxes[3][1].get()

        if self.AdminVar.get() != self.originalUserData[4]:
            data[2] = self.AdminVar.get()

        if data != [None for i in range(3)]:
            account_management.update_user_data(self.originalUserData[1], data[0], data[1], data[2])

        if self.entryBoxes[1][1].get() != "":
            if self.entryBoxes[1][1].get() != self.entryBoxes[2][1].get():
                errorLabel = tk.Label(self, text="ERROR - Passwords do not match", font=global_variables.text(12))
                errorLabel.grid(row=8, column=0, columnspan=2)
                return False
            elif len(self.entryBoxes[1][1].get()) < 8:
                errorLabel = tk.Label(self, text="ERROR - Passwords must be atleast 8 characters", font=global_variables.text(12))
                errorLabel.grid(row=8, column=0, columnspan=2)
                return False
            else:
                if data[0] is not None:
                    userName = data[0]
                else:
                    userName = self.originalUserData[1]
                account_management.update_user_password(userName, self.entryBoxes[1][1].get())

        self.parent.show_users()

    def deleteUserCommand(self):
        account_management.delete_user(self.originalUserData[1])
        self.parent.show_users()