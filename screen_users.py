import tkinter as tk

import account_management
import global_variables


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

        elif account_management.create_user(self.entryBoxes[0][1].get(), self.entryBoxes[1][1].get(), self.entryBoxes[3][1].get(), self.AdminVar.get()):
            self.parent.show_users()

        else:
            errorLabel = tk.Label(self, text="ERROR - Account creation failed", font=global_variables.text(12))
            errorLabel.grid(row=7, column=0, columnspan=2)

class UpdateUser(NewUser): #TODO modify new user frame to work as update user
    def __init__(self, parent, UserName):
        NewUser.__init__(self, parent)

        self.originalUserData = account_management.get_user_data(UserName)
        self.originalUserData[2] = ""

        self.entryBoxes[0][1].insert(0, self.originalUserData[1])
        self.entryBoxes[3][1].insert(0, self.originalUserData[3])

        for button in self.buttons:
            button.grid_forget()

        self.buttons = [tk.Button(self, text="Update User", font=global_variables.text(16), command=self.updateUserCommand)]
        self.buttons[0].grid(row=6, column=0, columnspan=2)

        self.buttons.append(tk.Button(self, text="Delete User", font=global_variables.text(16), command=self.deleteUserCommand))
        self.buttons[1].grid(row=7, column=0, columnspan=2)

        #TODO make the checkboxes actually work

    def updateUserCommand(self):
        pass

    def deleteUserCommand(self):
        pass
