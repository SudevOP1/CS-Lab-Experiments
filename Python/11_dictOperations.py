my_dict = {}
for i in range(3): my_dict[input(f"Key {i+1}: ")] = input(f"Value {i+1}: ")
print("Keys:")
for key in my_dict.keys(): print(key)
print("Values:")
for value in my_dict.values(): print(value)
print(f"Value for given the key = {my_dict[input("Enter a key: ")]}")