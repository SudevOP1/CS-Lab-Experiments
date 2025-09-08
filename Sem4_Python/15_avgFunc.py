def calculate_average(numbers):
    num_sum = 0
    for n in numbers:
        num_sum += n
    return num_sum / len(numbers)

size = int(input("Enter how many numbers to input: "))
input_nums = [int(input(f"Enter number {i+1}: ")) for i in range(size)]
input_avg = calculate_average(input_nums)
print(f"Avg of numbers = {input_avg}")