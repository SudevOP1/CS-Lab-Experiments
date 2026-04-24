import sqlite3

conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

def print_data():
    cursor.execute("SELECT * FROM Employees")
    data = cursor.fetchall()
    print(data)

employees_data = [
    (1, "Arthur", 28000),
    (2, "Micah", 24000),
    (3, "John", 21000),
]

cursor.execute("""
    CREATE TABLE Employees(
        id INTEGER PRIMARY KEY,
        name TEXT,
        salary INTEGER
    )
""")

cursor.executemany("""
    INSERT INTO Employees (id, name, salary)
    VALUES (?, ?, ?)
""", employees_data)
print_data()

cursor.execute("""
    UPDATE Employees
        SET salary = 30000
        WHERE name = "Micah"
""")
print_data()

cursor.execute("""
    DELETE FROM Employees
    WHERE name = "Micah"
""")
print_data()

conn.commit()
conn.close()