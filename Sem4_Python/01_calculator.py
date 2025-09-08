n1 = float(input("Enter first number : "))
n2 = float(input("Enter second number: "))
op = input("Enter operator     : ")[0]

if op == "+":               print(f"{n1} + {n2} = {n1+n2}")
elif op == "-":             print(f"{n1} - {n2} = {n1-n2}")
elif op == "*":             print(f"{n1} * {n2} = {n1*n2}")
elif op == "/" and n2 != 0: print(f"{n1} / {n2} = {n1/n2}")
elif op == "/" and n2 == 0: print("division by zero not allowed")