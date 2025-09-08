student = {
    "name": "Sudev",
    "roll": 69,
    "marks": 14,
}
print(student)
student["marks"] = int(input("Enter updated marks: "))
print(student)
student["grade"] = input("Enter grade: ")[0]
print(student)
del student["roll"]
print(student)