import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class EmployeeDetail(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)

        tk.Label(self, text="Employee Detail", font=("Arial", 20)).pack()