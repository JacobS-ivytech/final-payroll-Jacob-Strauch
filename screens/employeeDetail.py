import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sql import GetLastWeekDay, GetHours, GetSalary, UpdateHours, GetAllEmployees, PrefillWeekHours
from reportCalculations import CalculateGrossPay, CalculateNetPay
import datetime as dt


class EmployeeDetail(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller

        #get variable for specific user
        self.user = self.controller.currentUserId
        self.admin = self.controller.admin

        #get latest week to start payroll page on
        self.lastDayOfWeek = GetLastWeekDay()[0]

        self.weeks = [self.lastDayOfWeek]
        previousLastDay = self.lastDayOfWeek

        for i in range(4):
            previousLastDay = (dt.datetime.strptime(previousLastDay, "%Y-%m-%d") - dt.timedelta(days=7)).strftime("%Y-%m-%d")
            self.weeks.append(previousLastDay)

        #frame for top banner of page
        topBarFrame = tk.Frame(self)
        topBarFrame.pack(fill="both")

        for i in range(5):
            topBarFrame.grid_columnconfigure(i, weight=1)

        #frame for week selector group
        weekSelectorFrame = tk.Frame(topBarFrame)
        weekSelectorFrame.grid(column=0, row=0, sticky="w", padx=10)

         #Selector for week
        tk.Label(weekSelectorFrame, text="Week Ending on:").grid(column=0, row=0, padx=15, pady=15, sticky="w")
        self.weekSelector = ttk.Combobox(weekSelectorFrame, values=self.weeks, state="readonly")
        self.weekSelector.grid(column=1, row=0, sticky="w")
        self.weekSelector.set(self.lastDayOfWeek)
        ttk.Button(weekSelectorFrame, text="Select Week", command=lambda: self.LoadWeek()).grid(column=0, row=1, columnspan=2)
        
        #frame for employee selector group
        empSelectorFrame = tk.Frame(topBarFrame)
        empSelectorFrame.grid(column=1, row=0, sticky="w", padx=30)

        #get list of names for selector
        employees = GetAllEmployees()
        self.employeeMap = {}
        self.employeeDisplay = []
        for i in employees:
            display = f"{i.fname} {i.lname}"
            self.employeeDisplay.append(display)
            self.employeeMap[display] = i.id

        #Selector for employee
        tk.Label(empSelectorFrame, text="Employee to view:").grid(column=0, row=0, padx=15, pady=15, sticky="w")
        self.empSelector = ttk.Combobox(empSelectorFrame, values=self.employeeDisplay, state="readonly")
        self.empSelector.grid(column=1, row=0, sticky="w")
        self.empSelector.set(self.employeeDisplay[0])
        ttk.Button(empSelectorFrame, text="Select Employee", command=lambda: self.LoadEmployee()).grid(column=0, row=1, columnspan=2)
        
        #hides selector for nonadmin
        if self.admin == 0:
            empSelectorFrame.grid_remove()

        #Title of page
        tk.Label(topBarFrame, text="Employee Detail", font=("Arial", 20)).grid(column=2, row=0)

        #Frame for admin buttons
        adminBtnFrame = tk.Frame(topBarFrame)
        adminBtnFrame.grid(column=3, row=0)

        #button to lock week from edits
        lockBtn = ttk.Button(adminBtnFrame, text="Lock/Unlock Week", command=lambda: self.lockWeek)
        lockBtn.grid(column=0, row=0, pady=10)

        #button to load next week into system
        newWeekBtn = ttk.Button(adminBtnFrame, text="Build Next Week", command=lambda: PrefillWeekHours())
        newWeekBtn.grid(column=0, row=1)

        #hide buttons from non admin
        if self.admin == 0:
            adminBtnFrame.grid_remove()

        #Save Changes button
        saveBtn = ttk.Button(topBarFrame, text="Save and Calculate", command=lambda: self.CalculatePay())
        saveBtn.grid(column=4, row=0, sticky="e", padx=25)

        #frame for hours grid
        self.hourFrame = tk.Frame(self)
        self.hourFrame.pack(fill="both")

        #format columns
        self.hourFrame.grid_columnconfigure(0, weight=1)
        self.hourFrame.grid_columnconfigure(1, weight=1)
        self.hourFrame.grid_columnconfigure(2, weight=1)
        self.hourFrame.grid_columnconfigure(3, weight=1)
        self.hourFrame.grid_columnconfigure(4, weight=1)
        self.hourFrame.grid_columnconfigure(5, weight=1)
        self.hourFrame.grid_columnconfigure(6, weight=1)
        self.hourFrame.grid_columnconfigure(7, weight=1)

        #labels for each day of week
        tk.Label(self.hourFrame, text="Sunday", font=("Arial", 18)).grid(column=1, row=0, pady=25)
        tk.Label(self.hourFrame, text="Monday", font=("Arial", 18)).grid(column=2, row=0)
        tk.Label(self.hourFrame, text="Tuesday", font=("Arial", 18)).grid(column=3, row=0)
        tk.Label(self.hourFrame, text="Wednesday", font=("Arial", 18)).grid(column=4, row=0)
        tk.Label(self.hourFrame, text="Thursday", font=("Arial", 18)).grid(column=5, row=0)
        tk.Label(self.hourFrame, text="Friday", font=("Arial", 18)).grid(column=6, row=0)
        tk.Label(self.hourFrame, text="Saturday", font=("Arial", 18)).grid(column=7, row=0)

        #row Labels
        tk.Label(self.hourFrame, text="Date", font=("Arial", 18)).grid(column=0, row=1, pady=20)
        tk.Label(self.hourFrame, text="Hours", font=("Arial", 18)).grid(column=0, row=2, pady=20)
        tk.Label(self.hourFrame, text="PTO", font=("Arial", 18)).grid(column=0, row=3, pady=20)

        #load with most recent week hours
        self.LoadWeek()

        #tree for deductions
        self.payFrame = tk.Frame(self)
        self.payFrame.pack()

        #format tree
        self.tree = ttk.Treeview(self.payFrame, columns=("Deduction Type", "Deduction"), show="headings")
        self.tree.heading("Deduction Type", text="Deduction Type")
        self.tree.column("Deduction Type", width=200)
        self.tree.heading("Deduction", text="Deduction")
        self.tree.column("Deduction", width=150)

        self.tree.grid(column=0, row=0, padx=15)

        #frame for pay displays
        self.grossPayFrame = tk.Frame(self.payFrame)
        self.grossPayFrame.grid(column=1, row=0)

        #labels that display gross and net pay
        tk.Label(self.grossPayFrame, text="Gross Pay", font=("Arial", 18)).grid(column=0, row=0, padx=25)
        tk.Label(self.grossPayFrame, text="Net Pay", font=("Arial", 18)).grid(column=0, row=1)

        self.grossPayLabel = tk.Label(self.grossPayFrame, text="-", font=("Arial", 18), bg="white")
        self.grossPayLabel.grid(column=1, row=0, padx=25)
        self.netPayLabel = tk.Label(self.grossPayFrame, text="-", font=("Arial", 18), bg="white")
        self.netPayLabel.grid(column=1, row=1)



    def LoadWeek(self):

        result = GetHours(2, self.weekSelector.get()) ######################Change to SELF.USER
        salary = GetSalary(2)###############################################

        workingCol = 1

        #store entries for calculations later
        self.hours_entries = {}
        self.pto_entries = {}
        for item in result:
            empId, day, hours, pto, lock = item

            #date for day of week
            tk.Label(self.hourFrame, text=day, font=("Arial", 16)).grid(column=workingCol, row=1)

            #hours for date
            hours_entry = tk.Entry(self.hourFrame, font=("Arial", 16), width=6, justify="right")
            hours_entry.insert(0, hours)
            hours_entry.grid(column=workingCol, row=2)

            #pto for date
            pto_entry = tk.Entry(self.hourFrame, font=("Arial", 16), width=6, justify="right")
            pto_entry.insert(0, pto)
            pto_entry.grid(column=workingCol, row=3)

            #check if locked
            if lock == 1:
                hours_entry.config(state="disabled")
                pto_entry.config(state="disabled")
            
            #store entry
            self.hours_entries[day] = hours_entry
            self.pto_entries[day] = pto_entry

            #increment column
            workingCol += 1

    def LoadEmployee(self):
        selection = self.empSelector.get()
        empId = self.employeeMap[selection]
        self.user = empId
        self.LoadWeek()


    def CalculatePay(self):
        self.GatherHours()
        grossPay = CalculateGrossPay(2, self.weekSelector.get())#######################

        self.grossPayLabel.config(text=f"${grossPay:.2f}")

        #clear tree if has contents
        for item in self.tree.get_children():
            self.tree.delete(item)

        netPay, deductions = CalculateNetPay(2, grossPay)###############################4

        #insert deductions into tree
        for tax in deductions:
            self.tree.insert("", "end", values=(
                tax,
                f"${deductions[tax]:.2f}"
            ))

        #set label
        self.netPayLabel.config(text=f"${netPay:.2f}")

    def GatherHours(self):

        hoursPackage = []

        #validate hours before saving
        for day in self.hours_entries:
            try:
                hours = float(self.hours_entries[day].get())
                pto = float(self.pto_entries[day].get())
            except ValueError:
                messagebox.showerror(title="Error", message=f"Invalid input for {day}")
                return
            
            if hours > 12:
                messagebox.showerror(title="Error", message=f"Too many work hours for {day}. Must be less than 12.")
                return
            elif pto > 8:
                messagebox.showerror(title="Error", message=f"Too many PTO hours for {day}.")
                return
            elif hours < 0 or pto < 0:
                messagebox.showerror(title="Error", message=f"Must enter hours greater than or equal to 0 for {day}.")
                return
            
            #add validated hours to list
            hoursPackage.append((int(self.user), day, hours, pto))

        UpdateHours(hoursPackage)
