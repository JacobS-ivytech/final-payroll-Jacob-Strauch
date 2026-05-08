import sqlite3
import hashlib
from Employee import Employee

#get passord for user from database
def GetPassword(email):
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM employees WHERE email = ?",(email,))
    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]
    else:
        return None
    

#get admin status for given account
def GetAdminStatus(email):
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    cursor.execute("SELECT admin FROM employees WHERE email = ?",(email,))
    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]
    else:
        return None
    

def GetEmployee(email):
    pass


def GetAllEmployees():
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    #get all employees from database
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    connection.close()

    employeeList = []

    for employee in result:
        emp = Employee(
            employee[0],
            employee[1],
            employee[2],
            employee[3],
            employee[4],
            employee[5],
            employee[6],
            employee[7],
            employee[8],
            employee[9],
            employee[10],
            employee[11],
            employee[12],
            employee[13],
            employee[14],
            employee[15])
        employeeList.append(emp)

    return employeeList

    


def AddEmployee(emp):
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    #grab highest id number from table
    cursor.execute("SELECT MAX(id) FROM employees")
    highestId = cursor.fetchone()[0]
    newId = highestId + 1

    cursor.execute("""
    INSERT INTO employees (
    id, fname, lname, status, department, title,
    DoB, gender, payType, payRate, email, address, zip,
    dependents, admin, password
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        newId,
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
        emp.admin,
        emp.password
    ))
    connection.commit()
    connection.close()
    