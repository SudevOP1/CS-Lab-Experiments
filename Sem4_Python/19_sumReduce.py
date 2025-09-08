from functools import reduce

size = int(input("Enter how many numbers to input: "))
nums = [int(input(f"Enter number {i+1}: ")) for i in range(size)]

total = reduce(lambda x,y: x+y, nums)

print(f"Sum = {total}")