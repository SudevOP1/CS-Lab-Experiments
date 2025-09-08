arr = [
    [
        int(input(f"Enter element({i}, {j}): "))
        for j in range(3)
    ]
    for i in range(3)
]

print("\nEntered array:")
for row in arr:
    for elem in row:
        print(elem, end=" ")
    print("")

for i in range(len(arr)):
    row_sum = 0
    for j in range(len(arr)):
        row_sum += arr[i][j]
    print(f"Sum of row {i+1} = {row_sum}")

for i in range(len(arr)):
    col_sum = 0
    for j in range(len(arr)):
        col_sum += arr[j][i]
    print(f"Sum of col {i+1} = {col_sum}")