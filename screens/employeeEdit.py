import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class EmployeeEdit(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)

        tk.Label(self, text="Employee Edit", font=("Arial", 20)).pack()