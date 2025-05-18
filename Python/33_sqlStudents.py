import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

students_data = [
    ("Arthur", 28, "A"),
    ("Micah", 29, "D"),
    ("John", 23, "B"),
]

cursor.execute("""
    CREATE TABLE Students (
        name TEXT PRIMARY KEY,
        age INTEGER,
        grade TEXT
    )
""")

cursor.executemany("""
    INSERT INTO students
    (name, age, grade)
    VALUES (?, ?, ?)
""", students_data)
conn.commit()

cursor.execute("SELECT * FROM students")
all_students = cursor.fetchall()
print("Student Records:")
for student in all_students: print(student)

conn.close()