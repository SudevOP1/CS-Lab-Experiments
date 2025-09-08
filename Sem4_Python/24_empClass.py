class Employee:

    def __init__(self, name, employee_id, salary):
        self.name        = name
        self.employee_id = employee_id
        self.salary      = salary

    def show_details(self):
        print(f"Name       : {self.name}")
        print(f"Employee ID: {self.employee_id}")
        print(f"Salary     : {self.salary}")

    def increment_salary(self, percent):
        self.salary *= (100+percent)/100

emp1 = Employee("Sudev", 69, 69000)
emp2 = Employee("Vivian", 68, 20000)
emp1.increment_salary(20)
emp2.increment_salary(10)
emp1.show_details()
emp2.show_details()