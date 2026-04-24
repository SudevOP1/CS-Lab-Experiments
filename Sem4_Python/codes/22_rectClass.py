class Rectangle:

    def __init__(self, length, breadth):
        self.length  = length
        self.breadth = breadth

    def get_area(self):
        return self.length * self.breadth

    def get_perimeter(self):
        return 2 * (self.length + self.breadth)

rect = Rectangle(2, 3)
print(f"Area = {rect.get_area()}")
print(f"Perimeter = {rect.get_perimeter()}")