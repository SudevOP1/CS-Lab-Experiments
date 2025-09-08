size = int(input("Enter size of array: "))
arr = [int(input(f"Enter element {i+1}: ")) for i in range(size)]

print("\nArray = ", end="")
for elem in arr: print(elem, end=" ")

arr_sum = 0
for elem in arr: arr_sum += elem
print(f"\nSum of elements = {arr_sum}")

arr_max = -100000
for elem in arr:
    if elem > arr_max: arr_max = elem
print(f"Max element = {arr_max}")