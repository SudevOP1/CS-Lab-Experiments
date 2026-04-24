import tkinter as tk

def calculate_sum():
    num1 = entry1.get()
    num2 = entry2.get()
    if not num1 or not num2:
        result_label.config(text="Enter valid numbers!")
        return
    try: result_label.config(text=f"Sum = {float(num1)+float(num2)}")
    except Exception as e: result_label.config(text=f"Error: {e}")

window = tk.Tk()
window.geometry("300x150")
window.title("Sum Calculator")

label1 = tk.Label(window, text="Enter first num: ")
label1.pack(pady=0)
entry1 = tk.Entry(window)
entry1.pack(pady=0)

label2 = tk.Label(window, text="Enter second num: ")
label2.pack(pady=0)
entry2 = tk.Entry(window)
entry2.pack(pady=0)

sum_button = tk.Button(window, text="Calculate Sum", command=calculate_sum)
sum_button.pack(pady=10)

result_label = tk.Label(window, text="Sum: ")
result_label.pack(pady=0)

window.mainloop()