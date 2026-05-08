import sqlite3

connection = sqlite3.connect('ABC.db')

cursor = connection.cursor()

#create tables

command1 = """CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            status TEXT NOT NULL,
            department TEXT NOT NULL,
            title TEXT NOT NULL,
            DoB TEXT NOT NULL,
            gender TEXT NOT NULL,
            payType TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            zip TEXT NOT NULL,
            dependents INTEGER NOT NULL,
            admin INTEGER NOT NULL,
            password TEXT NOT NULL)"""

command2 = """CREATE TABLE IF NOT EXISTS deductions (
            type TEXT PRIMARY KEY,
            percent INTEGER NOT NULL)"""

command3 = """CREATE TABLE IF NOT EXISTS workhours (
            employee_id INTEGER NOT NULL,
            work_date TEXT NOT NULL,
            hours REAL NOT NULL CHECK(hours >= 0),
            locked INTEGER NOT NULL,
            PRIMARY KEY (employee_id, work_date),
            FOREIGN KEY (employee_id) REFERENCES employees(id))"""

cursor.execute(command1)
cursor.execute(command2)
cursor.execute(command3)

connection.close()