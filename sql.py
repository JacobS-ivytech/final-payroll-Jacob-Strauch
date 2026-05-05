import sqlite3
import hashlib

connection = sqlite3.connect('ABC.db')

cursor = connection.cursor()

#get passord for user from database
def GetPassword(email):
    cursor.execute("SELECT password FROM employees WHERE email = ?",(email,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None
    
def AddEmployee(emp):
    #grab highest id number from table
    cursor.execute("SELECT MAX(id) FROM employees")
    highestId = cursor.fetchone()[0]
    newId = highestId + 1

    cursor.execute("""
    INSERT INTO employees (
    id, fname, lname, status, department, title,
    DoB, gender, payType, email, address, zip,
    dependents, password
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        emp.email,
        emp.address,
        emp.zip,
        emp.dependents,
        emp.admin,
        emp.password
    ))
    connection.commit()
    

passwordhashed = hashlib.sha256('2000-01-01'.encode()).hexdigest()

#cursor.execute("""INSERT INTO employees VALUES
#               (1, 'Adam', 'Smith', 'active', 'laborer', 'associate', 
#               '2000-01-01', 'male', 'hourly', 'AdamSmith@ABC.com', '123 w. main st.',
#               '47305', 1, 0, ?)""", (passwordhashed,))
