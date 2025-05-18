my_list = [20, 10, 40, 30]

print(my_list, end="\n\n")

my_list.append(50)
print(my_list, end="\n\n")

my_list.sort()
print(my_list, end="\n\n")

my_list.remove(int(input("Which element to remove? ")))
print(my_list)