import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Payroll(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)

        tk.Label(self, text="Payroll", font=("Arial", 20)).pack()