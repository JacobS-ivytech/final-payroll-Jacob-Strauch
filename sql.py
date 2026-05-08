import sqlite3
import hashlib
from Employee import Employee
import datetime as dt

#get passord for user from database
def GetLoginData(email):
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    cursor.execute("SELECT password, id, admin FROM employees WHERE email = ?",(email,))
    result = cursor.fetchone()

    connection.close()

    if result:
        return result
    else:
        return None
        

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
    

def GetAllEmployeeIdPayType():
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    #get all employee ids
    cursor.execute("SELECT id, payType FROM employees")
    empIdPayType = cursor.fetchall()

    connection.close()
    return empIdPayType


def PrefillWeekHours(firstDay):
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    #get all employee ids
    empIdPayType = GetAllEmployeeIdPayType()

    #loop through all employees to fill
    for id, payType in empIdPayType:
        week=[]
        current = firstDay
        #check pay type to determine prefill hours
        if payType == "Salary":
            hour = 8
        else:
            hour = 0

        for i in range(7):
            day = (id, current, hour, 0, 0)
            week.append(day)
            current = (dt.datetime.strptime(current, "%Y-%m-%d") + dt.timedelta(days=1)).strftime("%Y-%m-%d")

        cursor.executemany("INSERT OR IGNORE INTO workhours VALUES (?, ?, ?, ?, ?)", week)
    
    connection.commit()
    connection.close()


def GetHours(empId, endDate):
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    #find start of week
    startDate = (dt.datetime.strptime(endDate, "%Y-%m-%d") - dt.timedelta(days=6)).strftime("%Y-%m-%d")

    #query db for weeks hours
    cursor.execute("SELECT * FROM workhours WHERE employee_id = ? AND work_date BETWEEN ? AND ?",
                   (empId, startDate, endDate))
    
    result = cursor.fetchall()
    connection.close()
    return result


def GetSalary(empId):
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    cursor.execute("SELECT payType FROM employees WHERE id = ?", (empId,))

    result = cursor.fetchone
    connection.close()
    return result

def GetLastWeekDay():
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT work_date 
                   FROM workhours 
                   ORDER BY work_date DESC
                   LIMIT 1""")
    
    latestDate = cursor.fetchone()
    connection.close()
    return latestDate

def GetPayInfo(empId):
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    cursor.execute("SELECT payRate, dependents FROM employees WHERE id = ?", (empId,))

    result = cursor.fetchone()
    connection.close()
    return result

def GetDeductions():
    connection = sqlite3.connect('ABC.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM deductions")

    result = cursor.fetchall()
    connection.close()
    return result