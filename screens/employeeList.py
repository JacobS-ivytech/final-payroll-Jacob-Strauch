import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sql import GetAllEmployees, FullDeleteEmployee
from screens.newEmployee import NewEmployee


class EmployeeListAll(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller

        #frame for top bar
        topBarFrame = tk.Frame(self)
        topBarFrame.pack(fill="x")

        topBarFrame.grid_columnconfigure(0, weight=1)
        topBarFrame.grid_columnconfigure(1, weight=1)
        topBarFrame.grid_columnconfigure(2, weight=1)

         #frame for employee selector group
        empSelectorFrame = tk.Frame(topBarFrame)
        empSelectorFrame.grid(column=0, row=0, sticky="w", padx=30)

        #get list of names for selector
        employees = GetAllEmployees()
        self.employeeMap = {}
        self.employeeDisplay = []
        for i in employees:
            display = f"{i.fname} {i.lname}"
            self.employeeDisplay.append(display)
            self.employeeMap[display] = i.id

        #Selector for employee
        self.empSelector = ttk.Combobox(empSelectorFrame, values=self.employeeDisplay, state="readonly")
        self.empSelector.grid(column=0, row=0, sticky="w", padx=25)
        self.empSelector.set("")
        ttk.Button(empSelectorFrame, text="Delete Employee", command=lambda: self.DeleteEmployee()).grid(column=1, row=0)

        tk.Label(topBarFrame, text="Employee List All", font=("Arial", 20)).grid(column=1, row=0)

        #button to add new employee screen
        self.test_btn = ttk.Button(
            topBarFrame, 
            text="Add Employee", 
            command=lambda: self.controller.show_frame("NewEmployee"))
        self.test_btn.grid(column=2, row=0, padx=20, pady=20, sticky="e")

        listFrame = tk.Frame(self)
        listFrame.pack(fill=tk.BOTH, expand=True)

        #define each labels content for reuse in building table
        columns = ("ID",
                    "First Name",
                    "Last Name",
                    "Status",
                    "Department",
                    "Title",
                    "Date of Birth",
                    "Gender",
                    "Pay Type",
                    "Pay Rate",
                    "Email",
                    "Address",
                    "Zip Code",
                    "Num. of Dependents",
                    "Admin Status")

        #create tree
        self.tree = ttk.Treeview(listFrame, columns=columns, show="headings")

        #format each column
        for item in columns:
            self.tree.heading(item, text=item)
            if item == "Email":
                self.tree.column(item, width = 120)
            elif item == "ID" or item == "Num. of Dependents" or item == "Admin Status":
                self.tree.column(item, width=40)
            elif item =="Title":
                self.tree.column(item, width=60)
            else:
                self.tree.column(item, width=40)

        self.refreshTree()



        self.tree.pack(fill=tk.BOTH, expand=True)

    def refreshTree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        employees = GetAllEmployees()

        for emp in employees:
            self.tree.insert("", "end", values=(
                emp.id,
                emp.fname,
                emp.lname,
                emp.status,
                emp.department,
                emp.title,
                emp.dob,
                emp.gender,
                emp.payType,
                emp.payRate,
                emp.email,
                emp.address,
                emp.zipCode,
                emp.dependents,
                emp.admin
            ))

    def DeleteEmployee(self):
        #get employee from selector
        selection = self.empSelector.get()
        empId = self.employeeMap[selection]

        #get confirmation before deleting
        confirm = messagebox.askyesno(
            title="Confirm Employee Delete",
            message="Are you sure you want to delete this employee?\nThis action can not be undone.")
        
        if not confirm:
            return
        
        #delete employee from db
        FullDeleteEmployee(empId)
        messagebox.showinfo(title="Success", message="Employee successfully deleted")
        self.refreshTree()
