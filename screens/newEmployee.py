import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import date
from sql import AddEmployee
from Employee import Employee
import hashlib


class NewEmployee(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller
    
        tk.Label(self, text="New Employee Sign Up", font=("Arial", 24)).pack(pady=15)

        self.form = tk.Frame(self)
        self.form.pack()

        #empty dict to store entries
        self.entries = {}
        
        #First Name
        tk.Label(self.form, text="First Name").grid(
            row=0, column=0, sticky="w")
        self.fname_entry = tk.Entry(self.form)
        self.fname_entry.grid(row=0, column=1, padx=10, pady=10)
        self.entries["First Name"] = self.fname_entry

        #Last Name
        tk.Label(self.form, text="Last Name").grid(
            row=1, column=0, sticky="w")
        self.lname_entry = tk.Entry(self.form)
        self.lname_entry.grid(row=1, column=1, padx=10, pady=10)
        self.entries["Last Name"] = self.lname_entry

        #Employment Status
        statuses = ["Active", "Terminated"]
        tk.Label(self.form, text="Status").grid(
            row=2, column=0, sticky="w")
        self.status_entry=ttk.Combobox(self.form, values=statuses, state="readonly")
        self.status_entry.grid(row=2, column=1, padx=10, pady=10)
        self.entries["Status"] = self.status_entry


        #Department
        departments = ["HR", "Maintenance", "Laborer", "Management"]
        tk.Label(self.form, text="Department").grid(
            row=3, column=0, sticky="w")
        self.department_entry=ttk.Combobox(self.form, values=departments, state="readonly")
        self.department_entry.grid(row=3, column=1, padx=10, pady=10)
        self.entries["Department"] = self.department_entry

        #Title
        tk.Label(self.form, text="Job Title").grid(
            row=4, column=0, sticky="w")
        self.jTitle_entry = tk.Entry(self.form)
        self.jTitle_entry.grid(row=4, column=1, padx=10, pady=10)
        self.entries["Job Title"] = self.jTitle_entry
        
        #requires new employee is atleast 18
        today = date.today()
        maxBirthday = date(
            today.year - 18,
            today.month,
            today.day
        )
        #date entry
        tk.Label(self.form, text="Date of Birth").grid(row=5, column=0, sticky="w")
        self.dob = DateEntry(self.form,
                  date_pattern="yyyy-mm-dd",
                  maxdate=maxBirthday)
        self.dob.grid(row=5, column=1)
        self.entries["Date of Birth"] = self.dob

        #gender entry
        genders = ["Male", "Female", "Other"]
        tk.Label(self.form, text="Gender").grid(
            row=6, column=0, sticky="w")
        self.gender_entry=ttk.Combobox(self.form, values=genders, state="readonly")
        self.gender_entry.grid(row=6, column=1, padx=10, pady=10)
        self.entries["Gender"] = self.gender_entry

        #paytype entry
        payTypes = ["Hourly", "Salary"]
        tk.Label(self.form, text="Pay Type").grid(
            row=7, column=0, sticky="w")
        self.payType_entry=ttk.Combobox(self.form, values=payTypes, state="readonly")
        self.payType_entry.grid(row=7, column=1, padx=10, pady=10)
        self.entries["Pay Type"] = self.payType_entry

        #payRate entry
        tk.Label(self.form, text="Pay Rate").grid(
            row=8, column=0, sticky="w")
        self.payRate_entry = tk.Entry(self.form)
        self.payRate_entry.grid(row=8, column=1, padx=10, pady=10)
        self.entries["Pay Rate"] = self.payRate_entry

        #Address entry
        tk.Label(self.form, text="Address").grid(
            row=9, column=0, sticky="w")
        self.address_entry = tk.Entry(self.form)
        self.address_entry.grid(row=9, column=1, padx=10, pady=10)
        self.entries["Address"] = self.address_entry

        #Zip entry
        tk.Label(self.form, text="Zip Code").grid(
            row=10, column=0, sticky="w")
        self.zip_entry = tk.Entry(self.form)
        self.zip_entry.grid(row=10, column=1, padx=10, pady=10)
        self.entries["Zip Code"] = self.zip_entry

        #dependents entry
        tk.Label(self.form, text="Number of Dependents").grid(
            row=11, column=0, sticky="w")
        self.dependents_entry = tk.Entry(self.form)
        self.dependents_entry.grid(row=11, column=1, padx=10, pady=10)
        self.entries["Dependents"] = self.dependents_entry

        #admin entry
        empTypes = ["Employee", "Admin"]
        tk.Label(self.form, text="Authorization Type").grid(
            row=12, column=0, sticky="w")
        self.admin_entry=ttk.Combobox(self.form, 
                                      textvariable=tk.StringVar(value = "Employee"), 
                                      values=empTypes,
                                      state="readonly")
        self.admin_entry.grid(row=12, column=1, padx=10, pady=10)
        self.entries["Admin"] = self.admin_entry

        save_btn = ttk.Button(self.form, text="Log Employee", command=lambda: self.GatherEmployee())
        save_btn.grid(row=13, column=0, columnspan=2)

    def GatherEmployee(self):

        #validate to check for empty input
        for key, value in self.entries.items():
            if value.get().strip() == "":
                messagebox.showerror(title="Error", message=f"Must provide input for {key}")
                return
        
        zip_code = self.entries["Zip Code"].get().strip()

        #check for format of zip entry
        if not zip_code.isdigit() or len(zip_code) != 5:
            messagebox.showerror(title="Error", message="Zip Code must be exactly 5 digits")
            return      
        
        depen = self.entries["Dependents"].get().strip()

        #check format of dependents entry
        if not depen.isdigit() or int(depen) < 0 or int(depen) > 9:
            messagebox.showerror(title="Error", message="Must enter single positive digit number for Dependents")
            return

        #check format of pay rate entry
        pay = self.entries["Pay Rate"].get().strip()
        try:
            pay_float = float(pay)
            if len(pay.split(".")) != 2 or len(pay.split(".")[1]) != 2:
                raise ValueError

        except ValueError:
            messagebox.showerror(title = "Error", message="Pay rate must be formatted like 15.75")
            return

        #prep names for email construction
        first = self.entries["First Name"].get().strip().lower()
        last = self.entries["Last Name"].get().strip().lower()

        #change format of admin variable for storage
        if self.entries["Admin"].get().strip().lower() == "admin":
            adminVar = 1
        else:
            adminVar = 0

        #gather birthday for password creation
        DoB = self.entries["Date of Birth"].get()
        hashedPassword = hashlib.sha256(DoB.encode()).hexdigest()

        newEmp = Employee(
            id=0,
            fname = first.capitalize(),
            lname = last.capitalize(),
            status = self.entries["Status"].get(),
            department = self.entries["Department"].get(),
            title = self.entries["Job Title"].get(),
            dob = DoB,
            gender = self.entries["Gender"].get(),
            payType = self.entries["Pay Type"].get(),
            payRate= pay,
            email =  f"{first}{last}@abc.com",
            address = self.entries["Address"].get(),
            zipCode = self.entries["Zip Code"].get(),
            dependents = int(depen),
            admin = adminVar,
            password = hashedPassword
        )

        try:
            #sql that adds employee to db
            AddEmployee(newEmp)

            #confirmation notice
            messagebox.showinfo(title="Success", message="New employee successfully added!")

            #clear all boxes
            for value in self.entries.values():
                if isinstance(value, tk.Entry):
                    value.delete(0, tk.END)
                elif isinstance(value, ttk.Combobox):
                    value.set("")
                elif isinstance(value, DateEntry):
                    value.set_date(date.today())
            
            self.controller.show_frame("EmployeeListAll")

        except Exception as e:
            messagebox.showerror(title="Database Error", message=str(e))