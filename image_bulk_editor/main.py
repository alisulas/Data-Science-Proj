import os
import random
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from tqdm import tqdm

def remove_exif(image):
    """
    Remove EXIF metadata from an image.

    Args:
        image (PIL.Image.Image): The original image.

    Returns:
        PIL.Image.Image: Image without EXIF data.
    """
    data = list(image.getdata())
    image_no_exif = Image.new(image.mode, image.size)
    image_no_exif.putdata(data)
    return image_no_exif

def apply_minimal_modifications(image):
    """
    Apply minimal modifications to an image to make it slightly unique.

    Modifications include:
    - Slightly adjusting brightness and contrast by ±2%
    - Applying a very subtle blur

    Args:
        image (PIL.Image.Image): The image to modify.

    Returns:
        PIL.Image.Image: Modified image.
    """
    # 1. Adjust Brightness by ±2%
    brightness_factor = 1.02 if random.choice([True, False]) else 0.98
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)

    # 2. Adjust Contrast by ±2%
    contrast_factor = 1.02 if random.choice([True, False]) else 0.98
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)

    # 3. Apply a very subtle blur (radius=0.5)
    image = image.filter(ImageFilter.GaussianBlur(radius=0.5))

    return image

def add_watermark(image, watermark_text=""):
    """
    Optionally add a subtle watermark to the image.

    Args:
        image (PIL.Image.Image): The image to watermark.
        watermark_text (str): Text to use as a watermark.

    Returns:
        PIL.Image.Image: Watermarked image.
    """
    if not watermark_text:
        return image  # No watermark added

    watermark = Image.new("RGBA", image.size)
    font_size = max(12, int(image.size[1] * 0.02))  # 2% of image height, minimum size 12
    try:
        draw = ImageDraw.Draw(watermark)

        # Use a truetype font if available
        try:
            # macOS default fonts path
            font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        text_width, text_height = draw.textsize(watermark_text, font)
        position = (image.size[0] - text_width - 10, image.size[1] - text_height - 10)  # Bottom-right corner

        draw.text(position, watermark_text, (255, 255, 255, 100), font=font)  # Semi-transparent white
        combined = Image.alpha_composite(image.convert("RGBA"), watermark)
        return combined.convert("RGB")
    except Exception as e:
        print(f"Failed to add watermark: {e}")
        return image

def process_image(input_path, output_path, add_wm=False, watermark_text=""):
    """
    Process a single image: remove EXIF, apply minimal modifications, and optionally add watermark.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the processed image.
        add_wm (bool): Whether to add a watermark.
        watermark_text (str): Text to use as a watermark.
    """
    try:
        with Image.open(input_path) as img:
            img = remove_exif(img)
            img = apply_minimal_modifications(img)
            if add_wm:
                img = add_watermark(img, watermark_text)
            img.save(output_path, quality=95)  # Save with high quality
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def batch_process_images(input_dir, output_dir, add_watermark_flag=False, watermark_text=""):
    """
    Batch process all images in the input directory.

    Args:
        input_dir (str): Directory containing input images.
        output_dir (str): Directory to save processed images.
        add_watermark_flag (bool): Whether to add watermark to all images.
        watermark_text (str): Text to use as a watermark.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')

    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_formats)]

    if not image_files:
        print("No images found in the input directory.")
        return

    print(f"Processing {len(image_files)} images...")

    for image_file in tqdm(image_files, desc="Processing Images"):
        input_path = os.path.join(input_dir, image_file)
        output_path = os.path.join(output_dir, image_file)
        process_image(input_path, output_path, add_wm=add_watermark_flag, watermark_text=watermark_text)

    print("Batch processing completed.")

if __name__ == "__main__":
    # Define input and output directories
    INPUT_DIR = "/Users/alisulas/Documents/BZNZ/Makeup/2"          # Your input directory path
    OUTPUT_DIR = "/Users/alisulas/Documents/BZNZ/output_images" # Your desired output directory path

    # Optional: Set watermark parameters
    ADD_WATERMARK = False            # Set to True to add a watermark
    WATERMARK_TEXT = "© YourName"    # Replace with your desired watermark text

    # Start batch processing
    batch_process_images(INPUT_DIR, OUTPUT_DIR, add_watermark_flag=ADD_WATERMARK, watermark_text=WATERMARK_TEXT)
