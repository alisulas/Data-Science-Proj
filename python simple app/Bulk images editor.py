import os
from PIL import Image, ImageEnhance, ImageOps
import cv2
import numpy as np

# Define your folder path
folder_path = "Users/alisulas/Documents/BZNZ/makeup"

# Function to modify images
def modify_image(image_path, output_path):
    image = Image.open(image_path)
    
    # Step 1: Crop the image (10% from each side)
    width, height = image.size
    left = width * 0.1
    top = height * 0.1
    right = width * 0.9
    bottom = height * 0.9
    image = image.crop((left, top, right, bottom))
    
    # Step 2: Adjust color, contrast, brightness
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.5)  # Increase color
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.3)  # Increase contrast
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)  # Increase brightness

    # Step 3: Apply rotation
    image = image.rotate(5)  # Rotate by 5 degrees

    # Step 4: Convert to grayscale and back to color to add noise
    grayscale = ImageOps.grayscale(image)
    image = ImageOps.colorize(grayscale, black="black", white="white")

    # Step 5: Add random noise using OpenCV
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    noise = np.random.normal(0, 25, image_cv.shape).astype(np.uint8)
    image_cv = cv2.add(image_cv, noise)
    image = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))

    # Save the modified image
    image.save(output_path)

# Iterate over images in the folder and modify them
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(folder_path, "modified_" + filename)
        modify_image(input_path, output_path)
        print(f"Modified image saved to: {output_path}")
