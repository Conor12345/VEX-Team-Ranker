import tkinter as tk

import global_variables

class NewUser(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        #TODO make new user frame

        nameLabel = tk.Label(self, text="New user", font=global_variables.text(16))
        nameLabel.grid(row=0, column=0, columnspan=2)

        self.entryBoxes = []
        labels = ["Username", "Password", "Repeated Password", "Team Number", "Admin"]

        for i in range(5):
            array = [tk.Label(self, text=labels[i], font=global_variables.text(12))]
            array[0].grid(row=i + 1, column=0)

            array.append(tk.Entry(self, font=global_variables.text(12)))
            array[1].grid(row=i + 1, column=1)


#TODO modify new user frame to work as update user