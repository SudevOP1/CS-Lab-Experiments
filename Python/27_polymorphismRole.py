class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, name, salary, role):
        super().__init__(name, salary)
        self.role = role
    def show_role(self):
        print(f"Role: {self.role}")

class Developer(Employee):
    def __init__(self, name, salary, role):
        super().__init__(name, salary)
        self.role = role
    def show_role(self):
        print(f"Role: {self.role}")

m = Manager("Sudev", 69000, "Project Manager")
d = Developer("Vivian", 55000, "Full Stack Developer")
for emp in [m, d]: emp.show_role()