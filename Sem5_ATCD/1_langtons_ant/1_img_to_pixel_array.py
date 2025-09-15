from PIL import Image
import json

def convert_img_to_pixel_array(pic_file_name, json_file_name):
    # Open the image and convert to grayscale
    with Image.open(pic_file_name) as img:
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
    with open(json_file_name, "w") as file:
        json.dump(my_dict, file)

    print(f"Grayscale pixel data saved to {json_file_name}")

if __name__ == "__main__":
    convert_img_to_pixel_array("hi_pic.png", "pixel_arrray.json")
