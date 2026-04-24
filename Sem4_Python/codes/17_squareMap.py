size = int(input("Enter how many numbers to input: "))
nums = [int(input(f"Enter number {i+1}: ")) for i in range(size)]

lambda_func = lambda x: (x*x)
sqrs = list(map(lambda_func, nums))

print("Original List: ", nums)
print("Squared List: ", sqrs)