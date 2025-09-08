from functools import reduce

size = int(input("Enter how many numbers to input: "))
nums = [int(input(f"Enter number {i+1}: ")) for i in range(size)]

maximum = reduce(lambda x,y: (x if x>y else y), nums)

print(f"Max = {maximum}")