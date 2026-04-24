my_tuple = tuple(int(input(f"Enter element {i+1}: ")) for i in range(5))

print("max =", {max(my_tuple)})
print("min =", {min(my_tuple)})
print("sum =", {sum(my_tuple)})
print("2nd =", {my_tuple[1]})
print("4th =", {my_tuple[3]})
