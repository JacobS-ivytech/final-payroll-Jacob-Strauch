import sqlite3 
import hashlib

connection = sqlite3.connect('ABC.db')

cursor = connection.cursor()

passwordhashed = hashlib.sha256('2000-01-01'.encode()).hexdigest()

cursor.execute("""INSERT INTO employees VALUES
               (1, 'Adam', 'Smith', 'Active', 'Laborer', 'Associate', 
               '2000-01-01', 'Male', 'Hourly', '20.00', 'adamsmith@abc.com', '123 w. main st.',
               '47305', 1, 0, ?)""", (passwordhashed,))

#cursor.execute("""INSERT INTO deductions VALUES
#               ('state tax', 315),('federal tax', 765),
#               ('social security tax', 620),('medicare', 145)
#""")

connection.commit()
cursor.execute("SELECT * FROM employees")
result = cursor.fetchall()
print(result)


connection.close()