import tkinter as tk
from tkinter import ttk
from screens.login import LoginPage
from screens.employeeDetail import EmployeeDetail
from screens.employeeList import EmployeeListAll
from screens.newEmployee import NewEmployee
from screens.payroll import Payroll

#Global Variables
primary_color = 'lightskyblue'
table_color = 'whitesmoke'
bg_color = 'aliceblue'

class PayrollApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ABC Company")

        #store current user and admin status identifier
        self.user = None
        self.admin = 0

        #basic setup of window
        self.geometry("1800x900")
        self.resizable(0, 0)
        self.config(bg=bg_color)

        #stylize buttons
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))

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
            command=lambda: self.show_frame("EmployeeListAll"))
        self.employee_list_btn.grid(column=0, row=0, padx=20, pady=20)

        #button to employee detail screen
        self.employeeDetailBtn = ttk.Button(
            self.menu, 
            text="Employee Pay Detail", 
            command=lambda: self.show_frame("EmployeeDetail"))
        self.employeeDetailBtn.grid(column=0, row=1, padx=20, pady=20)

        #button to payroll screen
        self.payrollBtn = ttk.Button(
            self.menu, 
            text="Payroll", 
            command=lambda: self.show_frame("Payroll"))
        self.payrollBtn.grid(column=0, row=3, padx=20, pady=20)

        #label for version
        tk.Label(self.menu, text="Version 1.0.0").grid(column=0, row=4, padx=40, pady=40, sticky="nsew")

        if self.admin == 0:
            self.employeeDetailBtn.grid_remove()
            self.employee_list_btn.grid_remove()
            self.payrollBtn.grid_remove()

        #main frame setup
        main_frame = tk.Frame(self)
        main_frame.place(relx=0.1, rely=0.1, relwidth=0.9, relheight=0.9)

        #frames for mainframe
        self.frames = {}

        #builds list of frames to switch between
        for F in (LoginPage, EmployeeDetail, EmployeeListAll, NewEmployee, Payroll):
            frame = F(main_frame, self)
            self.frames[F.__name__] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame("LoginPage")

    #pulls desired frame to the front of screen
    def show_frame(self, cont):
        frame = self.frames[cont]

        #refreshes list when going to page
        if cont == "EmployeeListAll":
            frame.refreshTree()
        elif cont == "EmployeeDetail":
            frame.OnShow()
            frame.RefreshEmpSelector()

        frame.tkraise()

    def refreshMenu(self):
        if self.admin == 1:
            self.employeeDetailBtn.grid()
            self.employee_list_btn.grid()
            self.payrollBtn.grid()

root = PayrollApp()
root.mainloop()