import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib
from sql import GetLoginData
from screens.employeeDetail import EmployeeDetail
from screens.employeeList import EmployeeListAll

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller

        #title
        tk.Label(self, text="Employee Login", font=("Arial", 16)).pack(pady=15)

        #form
        form = tk.Frame(self, bg="whitesmoke", padx=20, pady=20)
        form.pack(pady=10)

        #Email
        tk.Label(form, text="Email address:", bg="whitesmoke").grid(row=0, column=0, sticky="w")
        self.email_entry = ttk.Entry(form, width=30)
        self.email_entry.grid(row=1, column=0, pady=5)

        #Password
        tk.Label(form, text="Password:", bg="whitesmoke").grid(row=2, column=0, sticky="w")
        self.password_entry = ttk.Entry(form, show="*", width=30)
        self.password_entry.grid(row=3, column=0, pady=5)

        #radio buttons
        self.user_type = tk.StringVar(value="employee")

        tk.Label(form, text="Account Type:", bg="whitesmoke").grid(row=4, column=0, sticky="w", pady=(10, 0))

        tk.Radiobutton(form, text="Employee", variable=self.user_type, value="employee", bg="whitesmoke").grid(row=5, column=0, sticky="w")
        tk.Radiobutton(form, text="Admin", variable=self.user_type, value="admin", bg="whitesmoke").grid(row=6, column=0, sticky="w")

        tk.Button(form, text="Login", bg="lightskyblue", fg="black", command=self.login).grid(row=7, column=0, pady=15)

        #starts the cursor in the email box
        self.email_entry.focus()

    def login(self):
        email = self.email_entry.get().lower()
        password = self.password_entry.get()

        #gather hashed passwords
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()
        result = GetLoginData(email)

        if result is None:
            messagebox.showerror(title="Error", message="Wrong email or password")
            return
        else:
            storedPassword, currentId, adminStatus = result
        
        #checks if passwords match
        if hashedPassword == storedPassword:
            messagebox.showinfo(title='Login Success', message='You Successfully logged in')
            self.controller.user = currentId
            print("login" + str(self.controller.user))
            self.controller.admin = int(adminStatus)

            #check for admin status and redirect to appropriate page
            if adminStatus == 1:
                self.controller.show_frame("EmployeeListAll")
                self.controller.refreshMenu()
            else:
                self.controller.show_frame("EmployeeDetail")
        else:
            messagebox.showerror(title='Error', message='Wrong email or password')
