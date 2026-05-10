# final-payroll-Jacob-Strauch


## Description of App

This is an application to manage the employees and payroll for ABC company.

This application uses a sqlite3 database to store employee data that is then used in a fixed window graphic user interface within Python's Tkinter.

Employees can enter their hours worked for the week as well as PTO hours. The program then calculates their gross pay, each itemized deduction, and their net pay based of personalized information for each person.

An administrator has additonal access to tools to add, edit, and remove employees from the system. They can also adjust any employees hours. In their payroll window they can lock the employee's hours in their current state and create a report from those hours for payroll to be completed.


## Application Structure

The main app is titled "PayrollApp.py" and can be located in the root of this repository. In order to run the application just run this file and the window will open to the login screen.

All the classes used to build each screen viewed in the main window are located in the folder titled screens. 

Some of the scripts used to build and prefill the database are located in the folder called databaseSetup.

All of the supporting documents for this project including the project plan, blank test cases, completed test cases, **User Guide**, and UML documentation are located in the folder titled Supporting Documentation.
