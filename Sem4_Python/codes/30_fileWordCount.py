try:
    with open("temp.txt", "r") as file:
        file_contents = file.read()
        word_count = len(file_contents.split())
        print(f"There are {word_count} words in the file")

except Exception as e:
    print(f"An error occured: {e}")

finally:
    print("Program executed successfully")