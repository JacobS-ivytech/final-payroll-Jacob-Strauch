import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sql import GetLastWeekDay, GetHours, GetPayInfo, GetDeductions, GetSalary
import datetime as dt


class EmployeeDetail(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller

        self.user = self.controller.currentUserId

        #get latest week to start payroll page on
        self.lastDayOfWeek = GetLastWeekDay()[0]

        self.weeks = [self.lastDayOfWeek]
        previousLastDay = self.lastDayOfWeek

        for i in range(4):
            previousLastDay = (dt.datetime.strptime(previousLastDay, "%Y-%m-%d") - dt.timedelta(days=7)).strftime("%Y-%m-%d")
            self.weeks.append(previousLastDay)

        #frame for top banner of page
        topBarFrame = tk.Frame(self)
        topBarFrame.pack(fill="x")

        #frame for week selector group
        weekSelectorFrame = tk.Frame(topBarFrame)
        weekSelectorFrame.grid(column=0, row=0, sticky="w", padx=30)

        topBarFrame.grid_columnconfigure(0, weight=1)
        topBarFrame.grid_columnconfigure(1, weight=1)
        topBarFrame.grid_columnconfigure(2, weight=1)

        #Title of page
        tk.Label(topBarFrame, text="Employee Detail", font=("Arial", 20)).grid(column=1, row=0)

        #Selector for week
        tk.Label(weekSelectorFrame, text="Week Ending on:").grid(column=0, row=0, padx=15, pady=15, sticky="w")
        self.weekSelector = ttk.Combobox(weekSelectorFrame, values=self.weeks, state="readonly")
        self.weekSelector.grid(column=1, row=0, sticky="w")
        self.weekSelector.set(self.lastDayOfWeek)
        ttk.Button(weekSelectorFrame, text="Select Week", command=lambda: self.LoadWeek()).grid(column=0, row=1, columnspan=2)

        #Save Changes button
        saveBtn = ttk.Button(topBarFrame, text="Save and Calculate", command=lambda: self.CalculatePay())
        saveBtn.grid(column=2, row=0, sticky="e", padx=25)

        #frame for hours grid
        self.hourFrame = tk.Frame(self)
        self.hourFrame.pack(fill=tk.BOTH)

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

        self.payFrame = tk.Frame(self)
        self.payFrame.pack(fill=tk.BOTH)


    def LoadWeek(self):

        result = GetHours(1, self.weekSelector.get()) ######################Change to SELF.USER
        salary = GetSalary(1)###############################################

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

            #check if salaried
            if salary == 1:
                hours_entry.config(state="readonly")

            #check if locked
            if lock == 1:
                hours_entry.config(state="disabled")
                pto_entry.config(state="disabled")
            
            #store entry
            self.hours_entries[day] = hours_entry
            self.pto_entries[day] = pto_entry

            #increment column
            workingCol += 1

    def CalculatePay(self):
        payRate, dependents = GetPayInfo(1)###########################################

        #check hours before calculating pay
        for day in self.hours_entries:
            try:
                hours = float(self.hours_entries[day].get())
                pto = float(self.pto_entries[day].get())
            except ValueError:
                messagebox.showerror(title="Error", message=f"Invalid input for {day}")
            
            if hours > 12:
                messagebox.showerror(title="Error", message=f"Too many work hours for {day}. Must be less than 12.")
                return
            elif (hours + pto) > 8:
                messagebox.showerror(title="Error", message=f"Too many PTO hours for {day}.")
                return
            elif pto > 8:
                messagebox.showerror(title="Error", message=f"Too many PTO hours for {day}.")
                return
            elif hours < 0 or pto < 0:
                messagebox.showerror(title="Error", message=f"Must enter hours greater than or equal to 0 for {day}.")
                return

        grossPay = 0
        for i, day in enumerate(self.hours_entries):
            hours = float(self.hours_entries[day].get())
            if i == 0 or i == 6:
                #gives all day overtime pay for weekend work
                grossPay += hours * payRate * 1.5
            else:
                #gives straight pay for all hours worked
                grossPay += hours * payRate
                if hours > 8:
                    #gives extra 50% for overtime hours
                    grossPay += (hours - 8) * 0.5
        
        for day in self.pto_entries:
            #pays straight time pay for all pto hours
            grossPay += float(self.pto_entries[day].get()) * payRate

