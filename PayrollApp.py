import tkinter as tk
from tkinter import ttk
from screens.login import LoginPage
from screens.employeeDetail import EmployeeDetail
from screens.employeeList import EmployeeListAll
from screens.payroll import Payroll
from screens.newEmployee import NewEmployee

#Global Variables
primary_color = 'lightskyblue'
table_color = 'whitesmoke'
bg_color = 'aliceblue'

class PayrollApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ABC Company")

        #basic setup of window
        self.geometry("1800x900")
        self.resizable(0, 0)
        self.config(bg=bg_color)

        #header setup
        self.header = tk.Frame(self, bg= primary_color)
        self.header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.title_label = tk.Label(self.header, text="ABC Company", bg=bg_color, fg="black", font=("Arial", 24))
        self.title_label.pack(side="left", padx=10)
        self.close_btn = ttk.Button(self.header, text="X", command=self.destroy)
        self.close_btn.pack(side="right", padx=50, pady=10)

        #menu setup
        self.menu = tk.Frame(self, bg=primary_color)
        self.menu.place(relx=0, rely=0.1, relwidth=0.1, relheight=0.9)

        #button to employee list screen
        self.employee_list_btn = ttk.Button(
            self.menu, 
            text="Employee List", 
            command=lambda: self.show_frame(EmployeeListAll))
        self.employee_list_btn.pack(fill="x", padx=20, pady=20)

        #button to payroll screen
        self.payroll_btn = ttk.Button(
            self.menu, 
            text="Payroll", 
            command=lambda: self.show_frame(Payroll))
        self.payroll_btn.pack(fill="x", padx=20, pady=20)

        #button to payroll screen
        self.test_btn = ttk.Button(
            self.menu, 
            text="new emp", 
            command=lambda: self.show_frame(NewEmployee))
        self.test_btn.pack(fill="x", padx=20, pady=20)


        #main frame setup
        main_frame = tk.Frame(self)
        main_frame.place(relx=0.1, rely=0.1, relwidth=0.9, relheight=0.9)

        #frames for mainframe
        self.frames = {}

        #builds list of frames to switch between
        for F in (LoginPage, EmployeeDetail, EmployeeListAll, Payroll, NewEmployee): ########################################
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