my_str = input("Enter a string: ").lower()
palindrome = True;
for i in range(len(my_str) // 2):
    if my_str[i] != my_str[-i-1]:
        palindrome = False
        break
if palindrome: print("String is palindrome")
else: print("String is not palindrome")