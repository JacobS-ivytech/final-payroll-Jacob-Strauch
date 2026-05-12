import sqlite3 
import hashlib
import datetime as dt

connection = sqlite3.connect('ABC.db')

cursor = connection.cursor()

# passwordhashed = hashlib.sha256('6r848Ple99ac'.encode()).hexdigest()

# cursor.execute("""INSERT INTO employees VALUES
#                (1, 'Adam', 'Smith', 'Active', 'Laborer', 'Associate', 
#                '2000-01-01', 'Male', 'Hourly', '20.00', 'adamsmith@abc.com', '123 w. main st.',
#                '47305', 1, 0, ?)""", (passwordhashed,))

# cursor.execute("""INSERT INTO employees VALUES
#                (0, 'Main', 'Admin', 'Active', 'Laborer', 'Associate', 
#                '2005-01-01', 'Male', 'Hourly', '80.00', 'hr0001', '475 w. main st.',
#                '47305', 0, 1, ?)""", (passwordhashed,))

# cursor.execute("""INSERT OR IGNORE INTO deductions VALUES
#             ('State Tax', 315),('Federal Tax Employee', 765),
#             ('Social Security Tax Employee', 620),('Medicare Employee', 145),
#             ('Federal Tax Employer', 765), ('Social Security Tax Employer', 620),
#             ('Medicare Employer', 145)
# """)

# cursor.execute("DELETE FROM workhours")

week=[]
today = "2026-04-26"
for i in range(7):
    day = (1, today, 0, 0, 0)
    week.append(day)
    today = (dt.datetime.strptime(today, "%Y-%m-%d") + dt.timedelta(days=1)).strftime("%Y-%m-%d")

cursor.executemany("INSERT INTO workhours VALUES (?, ?, ?, ?, ?)", week)

connection.commit()
cursor.execute("SELECT * FROM workhours")
result = cursor.fetchall()
print(result)


# connection.close()