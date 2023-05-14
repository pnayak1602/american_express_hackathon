import os
from PIL import Image

# Specify the directory path where your images are located
directory = './extracted_eyes'

# Specify the desired dimensions
desired_width = 200
desired_height = 150

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Construct the full path to the image file
        image_path = os.path.join(directory, filename)

        # Open the image using PIL/Pillow
        image = Image.open(image_path)

        # Resize the image to the desired dimensions
        resized_image = image.resize((desired_width, desired_height))

        # Save the resized image with a new filename
        resized_image_path = os.path.join(directory, f"{filename}")
        resized_image.save(resized_image_path)

        # Optionally, display the resized image
        # resized_image.show()