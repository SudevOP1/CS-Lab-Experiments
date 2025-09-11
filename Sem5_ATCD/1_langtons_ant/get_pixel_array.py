from PIL import Image
import json

# Open the image and convert to grayscale
with Image.open("hi_pic.png") as img:
    img = img.convert("L")  # convert to grayscale
    width, height = img.size

    # Get all pixels as a flat list
    pixels = list(img.getdata())

    # Convert flat list to 2D list (list of rows)
    img_data = [pixels[i * width:(i + 1) * width] for i in range(height)]

# Create a dictionary to save
my_dict = {
    "data": img_data
}

# Write the pixel array to a JSON file
with open("img_data.json", "w") as file:
    json.dump(my_dict, file)

print("Grayscale pixel data saved to img_data.json")
