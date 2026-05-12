import tkinter as tk
from tkinter import ttk, messagebox
from sql import GetLastWeekDay, PrefillWeekHours, GetHours, LockWeek, GetAllEmployees
from reportCalculations import CalculateGrossPay, CalculateNetPay
import datetime as dt
import csv


class Payroll(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller

        #get variable for specific user
        self.user = self.controller.user
        self.admin = self.controller.admin

        #frame for top banner of page
        self.payrollFrame = tk.Frame(self)
        self.payrollFrame.pack(fill="both")

        for i in range(2):
            self.payrollFrame.grid_columnconfigure(i, weight=1)

        tk.Label(self.payrollFrame, text="Payroll Manager", font=("Arial", 24)).grid(column=0, row=0, columnspan=2, pady=25)

        #frame for week selector group
        self.weekSelectorFrame = tk.Frame(self.payrollFrame)
        self.weekSelectorFrame.grid(column=0, row=1, columnspan=2)

        #reset week selector
        self.ResetSelector()

        #set lock label accurately
        self.LockLabel()
        
        #button to prefill next week
        newWeekBtn = ttk.Button(self.payrollFrame, text="Build Next Week", command=lambda: self.AddWeek())
        newWeekBtn.grid(column=0, row=2, sticky="e")
        newWeekBtnLabel = tk.Label(self.payrollFrame, text="Generate the next week for employees to enter hours.\n" 
                                   "It will be prefilled with 8 for salaried workers and 0 for hourly.", 
                                   justify="left", anchor="w")
        newWeekBtnLabel.grid(column=1, row=2, pady=40, padx=25, sticky="w")

        #button to lock week
        lockBtn = ttk.Button(self.payrollFrame, text="Lock/Unlock Week", command=lambda: self.LockUnlock())
        lockBtn.grid(column=0, row=3, sticky="e")
        lockBtnLabel = tk.Label(self.payrollFrame, text="Lock the selected week hours from being edited by employees.\n" 
                                "Must lock hours before generating payroll report.", justify="left", anchor="w")
        lockBtnLabel.grid(column=1, row=3, pady=40, padx=25, sticky="w")

        #button to generate report
        reportBtn = ttk.Button(self.payrollFrame, text="Generate Payroll Report", command=lambda: self.GenerateReport())
        reportBtn.grid(column=0, row=4, sticky="e")
        reportBtnLabel = tk.Label(self.payrollFrame, text="Generate payroll report for all employees.\n" 
                                  "Report is saved in reports folder.", justify="left", anchor="w")
        reportBtnLabel.grid(column=1, row=4, pady=40, padx=25, sticky="w")

    def ResetSelector(self):

        # clear old widgets
        for widget in self.weekSelectorFrame.winfo_children():
            widget.destroy()

        #get latest week to start payroll page on
        self.lastDayOfWeek = GetLastWeekDay()[0]

        self.weeks = [self.lastDayOfWeek]
        previousLastDay = self.lastDayOfWeek

        for i in range(4):
            previousLastDay = (dt.datetime.strptime(previousLastDay, "%Y-%m-%d") - dt.timedelta(days=7)).strftime("%Y-%m-%d")
            self.weeks.append(previousLastDay)
            
        #Selector for week
        tk.Label(self.weekSelectorFrame, text="Week Ending on:", font=("Arial", 18)).grid(column=0, row=0, padx=15, pady=15, sticky="w")
        self.weekSelector = ttk.Combobox(self.weekSelectorFrame, values=self.weeks, state="readonly")
        self.weekSelector.grid(column=1, row=0)
        self.weekSelector.set(self.lastDayOfWeek)
        self.weekSelectorLock = tk.Label(self.weekSelectorFrame, text="", font=("Arial", 18), bg="white")
        self.weekSelectorLock.grid(column=0, row=1, columnspan=2)
        
    def AddWeek(self):
        PrefillWeekHours()
        self.ResetSelector()

    def LockLabel(self):
        #get hours from week and set values to list components
        hoursDb = GetHours(1, self.weekSelector.get())
        empId, date, hours, pto, locked = hoursDb[0]

        if locked == 0:
            self.weekSelectorLock.config(text="Unlocked")
        else:
            self.weekSelectorLock.config(text="Locked")

    def LockUnlock(self):
        #get hours from week and set values to list components
        hoursDb = GetHours(1, self.weekSelector.get())
        empId, date, hours, pto, locked = hoursDb[0]

        #Switched lock status of week
        LockWeek(self.weekSelector.get(), locked)
        
        self.LockLabel()

    def GenerateReport(self):
        employeeList = GetAllEmployees()

        #get week for report
        endDate = self.weekSelector.get()

        #build filename/path
        filename = f"reports/payroll_{endDate}.csv"

        if self.weekSelectorLock.cget("text") == "Unlocked":
            messagebox.showerror(title="Error", message="Must lock weeks hours before generating report")
            return

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            #header
            writer.writerow(["Employee Id", "First Name",
                            "Last Name", "Gross Pay", "Medical", "Stipend",
                            'State Tax','Federal Tax Employee', 
                            'Social Security Tax Employee', 'Medicare Employee',
                            'Federal Tax Employer', 
                            'Social Security Tax Employer', 'Medicare Employer', "---", 'Net Pay'])
            
            #loop through all employees writing lines for each
            for emp in employeeList:
                
                grossPay = CalculateGrossPay(emp.id, endDate)
                netPay, deductions = CalculateNetPay(emp.id, grossPay)

                writer.writerow([emp.id, emp.fname, emp.lname, f"{grossPay:.2f}",
                                 f"{deductions['Medical']}", f"{deductions['Stipend']}",
                                 f"{deductions['State Tax']:.2f}", f"{deductions['Federal Tax Employee']:.2f}",
                                 f"{deductions['Social Security Tax Employee']:.2f}", 
                                 f"{deductions['Medicare Employee']:.2f}", f"{deductions['Federal Tax Employer']:.2f}",
                                 f"{deductions['Social Security Tax Employer']:.2f}", 
                                 f"{deductions['Medicare Employer']:.2f}", "---", f"{netPay:.2f}"])
                
        messagebox.showinfo(title="Success", message=f"Report Successfully Genereated for {endDate}")
        return filename
        
