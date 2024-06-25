import argparse
from PIL import Image, ImageFilter
import os
import glob
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None
def compress_image(image_file, input_folder, quality):
    """
    Compresses the image with the specified quality while maintaining image size.
    Converts all images to JPEG format.
    """
    quality = int(quality)
    if not os.path.exists(os.path.join(input_folder, "compressed")):
        os.makedirs(os.path.join(input_folder, "compressed"))

    # Open the image
    image = Image.open(image_file)

    # Convert all images to JPEG format
    output_format = "JPEG"

    # Check if the image has an alpha channel
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        # Create a white background image of the same size as the original image
        background = Image.new("RGB", image.size, (255, 255, 255))

        # Composite the original image onto the white background
        background.paste(image, mask=image.split()[3])

        # Use the white background image as the compressed image
        compressed_image = background.copy()
    else:
        # Use the original image as the compressed image
        compressed_image = image.copy()

    # Save the compressed image as JPEG
    output_filename = os.path.splitext(os.path.basename(image_file))[0] + ".jpg"
    output_path = os.path.join(input_folder, "compressed", output_filename)
    compressed_image.save(output_path, format=output_format, quality=quality, optimize=True)

    # Close the images
    image.close()
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        background.close()

    return compressed_image


def convert_to_instagram_aspect_ratio(image_path, aspect_ratio):
    # Open the image
    image = Image.open(image_path)

    # Calculate the new size for the custom aspect ratio
    width, height = image.size
    aspect_width, aspect_height = map(int, aspect_ratio.split(':'))
    if aspect_width == 1 or aspect_height == 1:
        new_size = max(width, height)
    else:
        new_width = min(width, height * aspect_width // aspect_height)
        new_height = min(height, width * aspect_height // aspect_width)
        new_size = max(new_width, new_height)

    # Create a blurred copy of the original image
    blurred_image = image.copy()
    blurred_image = blurred_image.filter(ImageFilter.GaussianBlur(radius=30))

    # Resize the blurred image to fit the square image
    blurred_image = blurred_image.resize((new_size, new_size))

    # Create a new image with RGBA mode
    new_image = Image.new("RGBA", (new_size, new_size))

    # Paste the blurred image onto the new image as the background
    new_image.paste(blurred_image, (0, 0))

    # Calculate the offsets to center the original image
    x_offset = (new_size - width) // 2
    y_offset = (new_size - height) // 2

    # Paste the original image onto the new image as the foreground
    new_image.paste(image, (x_offset, y_offset))

    # Close the images
    image.close()
    blurred_image.close()

    return new_image


def convert_images(input_folder, aspect_ratio):
    # Get all image files in the input folder
    image_files = glob.glob(os.path.join(input_folder, "*.jpg")) + glob.glob(
        os.path.join(input_folder, "*.jpeg")) + glob.glob(os.path.join(input_folder, "*.png"))

    if len(image_files) > 0:
        # Convert images with progress bar
        with tqdm(total=len(image_files), desc="Converting images", unit="image") as pbar:
            for i, image_file in enumerate(image_files):
                # Convert image to Instagram aspect ratio
                converted_image = convert_to_instagram_aspect_ratio(image_file, aspect_ratio)

                # Create the 'converted' subdirectory if it doesn't exist
                converted_folder = os.path.join(input_folder, "converted")
                if not os.path.exists(converted_folder):
                    os.makedirs(converted_folder)

                # Save the converted image as PNG
                output_path = os.path.join(converted_folder, os.path.splitext(os.path.basename(image_file))[0] + ".png")
                converted_image.save(output_path, "PNG")

                # Update the progress bar
                pbar.update(1)

        print("Image conversion complete!")
        print(f"Converted images saved in the 'converted' subdirectory of the input folder.")
    else:
        print("No image files found in the input folder.")


def compress_images(input_folder, compression_percentage):
    # Get all image files in the input folder
    image_files = glob.glob(os.path.join(input_folder, "*.jpg")) + glob.glob(
        os.path.join(input_folder, "*.jpeg")) + glob.glob(os.path.join(input_folder, "*.png"))

    if len(image_files) > 0:
        # Compress images with progress bar
        with tqdm(total=len(image_files), desc="Compressing images", unit="image") as pbar:
            for i, image_file in enumerate(image_files):
                # Compress the image
                compressed_image = compress_image(image_file, input_folder, compression_percentage)

                # Save the compressed image only if it is a JPEG file
                if compressed_image.format == "JPEG":
                    output_path = os.path.join(input_folder, "compressed", os.path.basename(image_file))
                    compressed_image.save(output_path)

                # Update the progress bar
                pbar.update(1)

        print("Image compression complete!")
        print("Only JPEG images saved in the 'compressed' subdirectory of the input folder.")
    else:
        print("No image files found in the input folder.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Aspect Ratio Converter and Compressor")
    parser.add_argument("-i", "--input", type=str, help="Input folder containing images", required=True)
    parser.add_argument("-a", "--aspect-ratio", type=str, help="Custom aspect ratio (e.g., 4:3)", default="0:0")
    parser.add_argument("-q", "--quality", type=int, help="Reduce Quality (lossless) by Compression percentage (0-100)", default=0)
    args = parser.parse_args()

    input_folder = args.input
    aspect_ratio = args.aspect_ratio
    compression_percentage = args.quality

    if compression_percentage > 0 and aspect_ratio != "0:0":
        # Convert and compress images
        convert_images(input_folder, aspect_ratio)
        compress_images(os.path.join(input_folder, "converted"), compression_percentage)
    elif compression_percentage > 0:
        # Only compress images
        compress_images(input_folder, compression_percentage)
    elif aspect_ratio != "0:0":
        # Only convert aspect ratio
        convert_images(input_folder, aspect_ratio)
    else:
        print("No operation selected. Please provide a valid aspect ratio or compression percentage.")
