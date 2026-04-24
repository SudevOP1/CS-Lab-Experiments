try:
    file_contents = input("Enter file content string: ")
    with open("user_input.txt", "w") as file:
        file.write(file_contents)

    # # to confirm FileNotFoundError is handled
    # import os
    # os.remove("user_input.txt")

    with open("user_input.txt", "r") as file:
        content = file.read()
        print("File contents:", content)

except FileNotFoundError as e:
    print("File not found")

except IOError as e:
    print("I/O Error Occured")

finally:
    print("Program executed successfully")