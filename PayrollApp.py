import tkinter as tk
from tkinter import ttk
from login import LoginPage

#Global Variables
primary_color = 'lightskyblue'
table_color = 'whitesmoke'
bg_color = 'aliceblue'

class PayrollApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ABC Company")

        #basic setup of window
        self.geometry("1400x900")
        self.resizable(0, 0)
        self.config(bg=bg_color)

        #header setup
        self.header = tk.Frame(self, bg= primary_color)
        self.header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.title = tk.Label(self.header, text="ABC Company", bg=bg_color, fg="black", font=("Arial", 24))
        self.title.pack(side="left", padx=10)
        self.close_btn = ttk.Button(self.header, text="X", command=self.destroy)
        self.close_btn.pack(side="right", padx=50, pady=10)

        #menu setup
        self.menu = tk.Frame(self, bg=primary_color)
        self.menu.place(relx=0, rely=0.1, relwidth=0.15, relheight=0.9)

        #main frame setup
        main_frame = tk.Frame(self)
        main_frame.place(relx=0.15, rely=0.1, relwidth=0.85, relheight=0.9)

        #frames for mainframe
        self.frames = {}

        #builds list of frames to switch between
        for F in (LoginPage,): ########################################
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(LoginPage)

    #pulls desired frame to the front of screen
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


root = PayrollApp()
root.mainloop()