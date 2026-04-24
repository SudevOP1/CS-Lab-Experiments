import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = {
    "Name": ["Sudev", "Arthur", "John", "Micah", "Dutch"],
    "Marks": [100, 92, 78, 88, 90]
}
df = pd.DataFrame(data)

print("Student Data:")
print(df)
print(f"\nAverage Marks: {np.mean(df["Marks"])}")
print(f"Maximum Marks: {np.max(df["Marks"])}")
print(f"Minimum Marks: {np.min(df["Marks"])}")

plt.bar(df["Name"], df["Marks"], color="skyblue")
plt.title("Student Marks")
plt.xlabel("Students")
plt.ylabel("Marks")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()