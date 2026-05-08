import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sql import PrefillWeekHours, GetLastWeekDay


class Payroll(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__( parent)
        self.controller = controller

        #get latest week to start payroll page on
        self.lastDayOfWeek = GetLastWeekDay()

        tk.Label(self, text="Payroll", font=("Arial", 20)).pack()


    def LoadNextWeek(self):
        fjk