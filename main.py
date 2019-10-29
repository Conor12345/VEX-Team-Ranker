import tkinter as tk

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

        for F in [Login]:
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

app = Main()
app.mainloop()