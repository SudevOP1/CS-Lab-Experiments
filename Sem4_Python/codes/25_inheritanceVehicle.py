class Vehicle:

    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def disp_details(self):
        print(f"Brand: {self.brand}")
        print(f"Year : {self.year}")

class Car(Vehicle):

    def __init__(self, brand, year, model):
        super().__init__(brand, year)
        self.model = model

    def disp_details(self):
        super().disp_details()
        print(f"Model: {self.model}")

class Bike(Vehicle):

    def __init__(self, brand, year, type):
        super().__init__(brand, year)
        self.type = type

    def disp_details(self):
        super().disp_details()
        print(f"Type : {self.type}")