import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sql import GetAllEmployees


class EmployeeListAll(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller

        tk.Label(self, text="Employee List All", font=("Arial", 20)).pack(pady=15)

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

        