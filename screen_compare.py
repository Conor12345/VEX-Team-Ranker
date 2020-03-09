import tkinter as tk
import global_variables
from math import ceil

class Compare(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

    def bindSetup(self):
        self.selectedForCompare = self.controller.selectedForCompare # Store team list locally
        numTeams = len(self.selectedForCompare)
        rowNum = 0 # Row counter to be incremented after use

        returnButton = tk.Button(self, text="Return", font=global_variables.text(), command=self.goBack)
        returnButton.grid(row=rowNum, column=0, sticky="W", padx=10, pady=10, columnspan=100)
        rowNum += 1

        self.boxes = [] # Generate empty array
        for row1 in range(int(ceil(numTeams / 2))): # Loop for top row
            self.boxes.append(tk.Frame(self, padx=5, pady=5)) # Create empty frame
            self.boxes[-1].grid(row=rowNum, column=2*row1, columnspan=2) # Place empty frame on grid
        rowNum += 1 # Move onto next row

        if numTeams % 2 == 0: # If num of teams on second row is even
            wid = 2
        else:
            if numTeams == 3:
                wid = 4
            else:
                wid = 3

        for row2 in range(int(numTeams - (numTeams / 2))): # Loop for bottom row
            self.boxes.append(tk.Frame(self, padx=5, pady=5)) # Create empty frame
            self.boxes[-1].grid(row=rowNum, column=mul*row2, columnspan=wid) # Place empty frame on grid
        rowNum += 1

        self.labels = []
        for box in self.boxes:
            self.labels.append(tk.Label(box, text="Testing123"))
            self.labels[-1].grid(row=0, column=0)

    def goBack(self):
        for box in self.boxes:
            box.grid_forget()
        self.controller.show_frame(self.controller.currentFrame)