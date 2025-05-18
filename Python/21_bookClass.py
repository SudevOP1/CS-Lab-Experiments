class Book:

    def __init__(self, title, author, price):
        self.title  = title
        self.author = author
        self.price  = price

    def display_book(self):
        print("=============================")
        print(f"Title : {self.title}")
        print(f"author: {self.author}")
        print(f"price : {self.price}")

book1 = Book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 499)
book2 = Book("The Lord of the Rings", "J.R.R. Tolkien", 799)

book1.display_book()
book2.display_book()